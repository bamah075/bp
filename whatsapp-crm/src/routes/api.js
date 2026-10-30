// JSON API used by the dashboard (public/app.js)
const express = require('express');
const db = require('../db');
const { getChannel } = require('../channels');
const msg = require('../services/messages');
const { processInbound } = require('../services/bot');
const { runDueFollowups } = require('../services/scheduler');

const router = express.Router();
const wrap = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);
const q = () => db.get();

class HttpError extends Error {
  constructor(status, message) { super(message); this.status = status; }
}
const must = (row, what = 'Not found') => { if (!row) throw new HttpError(404, what); return row; };

// Build "UPDATE table SET a = ?, b = ?" from only the allowed fields present in the body
function patch(table, id, body, allowed, touch = false) {
  const keys = allowed.filter((k) => body[k] !== undefined);
  if (!keys.length) return;
  const sets = keys.map((k) => `${k} = ?`);
  if (touch) sets.push("updated_at = datetime('now')");
  q().prepare(`UPDATE ${table} SET ${sets.join(', ')} WHERE id = ?`).run(...keys.map((k) => body[k]), id);
}

// ---------- Status / dashboard ----------
router.get('/status', (req, res) => {
  const one = (sql, ...p) => q().prepare(sql).get(...p);
  res.json({
    live: getChannel('whatsapp').isLive(),
    stats: {
      contacts: one('SELECT COUNT(*) AS n FROM contacts').n,
      unread: one('SELECT COALESCE(SUM(unread),0) AS n FROM contacts').n,
      pendingFollowups: one("SELECT COUNT(*) AS n FROM followups WHERE status = 'pending'").n,
      openDeals: one("SELECT COUNT(*) AS n, COALESCE(SUM(value),0) AS v FROM deals d JOIN stages s ON s.id = d.stage_id WHERE s.name NOT IN ('Won','Lost')"),
      wonValue: one("SELECT COALESCE(SUM(value),0) AS v FROM deals d JOIN stages s ON s.id = d.stage_id WHERE s.name = 'Won'").v,
    },
  });
});

// ---------- Contacts ----------
const CONTACT_FIELDS = ['name', 'email', 'tags', 'notes', 'social', 'bot_paused'];

router.get('/contacts', (req, res) => {
  const where = [];
  const params = [];
  if (req.query.q) {
    where.push('(c.name LIKE ? OR c.phone LIKE ? OR c.email LIKE ? OR c.notes LIKE ?)');
    params.push(...Array(4).fill(`%${req.query.q}%`));
  }
  if (req.query.tag) {
    where.push("(',' || c.tags || ',') LIKE ?");
    params.push(`%,${req.query.tag},%`);
  }
  const rows = q().prepare(`
    SELECT c.*,
      (SELECT body FROM messages m WHERE m.contact_id = c.id ORDER BY m.id DESC LIMIT 1) AS last_message,
      (SELECT COUNT(*) FROM deals d WHERE d.contact_id = c.id) AS deal_count
    FROM contacts c ${where.length ? 'WHERE ' + where.join(' AND ') : ''}
    ORDER BY COALESCE(c.last_message_at, c.created_at) DESC LIMIT 500`).all(...params);
  res.json(rows.map((c) => ({ ...c, in_window: msg.inServiceWindow(c) })));
});

router.get('/contacts/export.csv', (req, res) => {
  const rows = q().prepare('SELECT name, phone, email, tags, notes, source, created_at FROM contacts ORDER BY id').all();
  const cell = (v) => `"${String(v ?? '').replaceAll('"', '""')}"`;
  const csv = ['name,phone,email,tags,notes,source,created_at', ...rows.map((r) => Object.values(r).map(cell).join(','))].join('\n');
  res.type('text/csv').attachment('contacts.csv').send(csv);
});

router.post('/contacts', (req, res) => {
  const phone = msg.normalizePhone(req.body.phone);
  if (!phone) throw new HttpError(400, 'Phone number is required (international format, e.g. 6591234567)');
  if (q().prepare('SELECT 1 FROM contacts WHERE phone = ?').get(phone)) throw new HttpError(409, 'A contact with this phone already exists');
  const { contact } = msg.upsertContact({ phone, name: req.body.name || '', source: req.body.source || 'manual' });
  patch('contacts', contact.id, req.body, ['email', 'tags', 'notes']);
  res.status(201).json(msg.getContact(contact.id));
});

router.get('/contacts/:id', (req, res) => {
  const c = must(msg.getContact(req.params.id));
  res.json({ ...c, in_window: msg.inServiceWindow(c) });
});

router.patch('/contacts/:id', (req, res) => {
  must(msg.getContact(req.params.id));
  const body = { ...req.body };
  if (body.social && typeof body.social === 'object') body.social = JSON.stringify(body.social);
  if (body.bot_paused !== undefined) body.bot_paused = body.bot_paused ? 1 : 0;
  patch('contacts', req.params.id, body, CONTACT_FIELDS, true);
  res.json(msg.getContact(req.params.id));
});

router.delete('/contacts/:id', (req, res) => {
  q().prepare('DELETE FROM contacts WHERE id = ?').run(req.params.id);
  res.sendStatus(204);
});

router.post('/contacts/:id/read', (req, res) => {
  q().prepare('UPDATE contacts SET unread = 0 WHERE id = ?').run(req.params.id);
  res.sendStatus(204);
});

// ---------- Messages ----------
router.get('/contacts/:id/messages', (req, res) => {
  res.json(q().prepare('SELECT * FROM messages WHERE contact_id = ? ORDER BY id DESC LIMIT 300').all(req.params.id).reverse());
});

router.post('/contacts/:id/messages', wrap(async (req, res) => {
  must(msg.getContact(req.params.id));
  const { body, templateName, templateLang, templateParams } = req.body;
  try {
    const m = await msg.sendMessage(Number(req.params.id),
      templateName ? { templateName, templateLang, templateParams: templateParams || [] } : { body }, 'agent');
    res.status(201).json(m);
  } catch (err) {
    throw new HttpError(502, `WhatsApp send failed: ${err.message}`);
  }
}));

// ---------- Pipeline: stages ----------
router.get('/stages', (req, res) => {
  res.json(q().prepare('SELECT * FROM stages ORDER BY position, id').all());
});

router.post('/stages', (req, res) => {
  if (!req.body.name) throw new HttpError(400, 'Stage name is required');
  const pos = q().prepare('SELECT COALESCE(MAX(position), -1) + 1 AS p FROM stages').get().p;
  const { lastInsertRowid } = q().prepare('INSERT INTO stages (name, position, color) VALUES (?, ?, ?)')
    .run(req.body.name, pos, req.body.color || '#64748b');
  res.status(201).json(q().prepare('SELECT * FROM stages WHERE id = ?').get(lastInsertRowid));
});

router.patch('/stages/:id', (req, res) => {
  patch('stages', req.params.id, req.body, ['name', 'position', 'color']);
  res.json(must(q().prepare('SELECT * FROM stages WHERE id = ?').get(req.params.id)));
});

router.delete('/stages/:id', (req, res) => {
  const n = q().prepare('SELECT COUNT(*) AS n FROM deals WHERE stage_id = ?').get(req.params.id).n;
  if (n) throw new HttpError(409, `Move the ${n} deal(s) out of this stage first`);
  q().prepare('DELETE FROM stages WHERE id = ?').run(req.params.id);
  res.sendStatus(204);
});

// ---------- Pipeline: deals ----------
const DEAL_SELECT = `SELECT d.*, c.name AS contact_name, c.phone AS contact_phone
  FROM deals d LEFT JOIN contacts c ON c.id = d.contact_id`;

router.get('/deals', (req, res) => {
  const rows = req.query.contactId
    ? q().prepare(`${DEAL_SELECT} WHERE d.contact_id = ? ORDER BY d.updated_at DESC`).all(req.query.contactId)
    : q().prepare(`${DEAL_SELECT} ORDER BY d.updated_at DESC`).all();
  res.json(rows);
});

router.post('/deals', (req, res) => {
  const { title, value = 0, contact_id = null, notes = '' } = req.body;
  if (!title) throw new HttpError(400, 'Deal title is required');
  const stage_id = req.body.stage_id || q().prepare('SELECT id FROM stages ORDER BY position LIMIT 1').get()?.id || null;
  const { lastInsertRowid } = q().prepare('INSERT INTO deals (title, value, contact_id, stage_id, notes) VALUES (?, ?, ?, ?, ?)')
    .run(title, Number(value) || 0, contact_id || null, stage_id, notes);
  res.status(201).json(q().prepare(`${DEAL_SELECT} WHERE d.id = ?`).get(lastInsertRowid));
});

router.patch('/deals/:id', (req, res) => {
  patch('deals', req.params.id, req.body, ['title', 'value', 'contact_id', 'stage_id', 'notes'], true);
  res.json(must(q().prepare(`${DEAL_SELECT} WHERE d.id = ?`).get(req.params.id)));
});

router.delete('/deals/:id', (req, res) => {
  q().prepare('DELETE FROM deals WHERE id = ?').run(req.params.id);
  res.sendStatus(204);
});

// ---------- Follow-ups ----------
router.get('/followups', (req, res) => {
  const params = [];
  let where = '';
  if (req.query.status) { where = 'WHERE f.status = ?'; params.push(req.query.status); }
  if (req.query.contactId) { where += (where ? ' AND' : 'WHERE') + ' f.contact_id = ?'; params.push(req.query.contactId); }
  res.json(q().prepare(`SELECT f.*, c.name AS contact_name, c.phone AS contact_phone
    FROM followups f JOIN contacts c ON c.id = f.contact_id ${where}
    ORDER BY CASE f.status WHEN 'pending' THEN 0 ELSE 1 END, f.send_at DESC LIMIT 500`).all(...params));
});

// Schedule for one contact (contactId) or every contact with a tag (tag)
router.post('/followups', (req, res) => {
  const { contactId, tag, body = '', templateName = '', templateLang = 'en_US', templateParams = '', sendAt, delayMinutes, cancelOnReply = true } = req.body;
  if (!body.trim() && !templateName) throw new HttpError(400, 'Write a message or choose a template');

  const when = sendAt ? new Date(sendAt) : new Date(Date.now() + (Number(delayMinutes) || 0) * 60000);
  if (Number.isNaN(when.getTime())) throw new HttpError(400, 'Invalid send time');

  let ids = [];
  if (contactId) ids = [must(msg.getContact(contactId), 'Contact not found').id];
  else if (tag) ids = q().prepare("SELECT id FROM contacts WHERE (',' || tags || ',') LIKE ?").all(`%,${tag},%`).map((r) => r.id);
  if (!ids.length) throw new HttpError(400, 'No matching contacts');

  const ins = q().prepare(`INSERT INTO followups (contact_id, body, template_name, template_lang, template_params, send_at, cancel_on_reply)
    VALUES (?, ?, ?, ?, ?, ?, ?)`);
  for (const id of ids) ins.run(id, body, templateName, templateLang, templateParams, msg.sqlTime(when), cancelOnReply ? 1 : 0);
  res.status(201).json({ scheduled: ids.length, sendAt: when.toISOString() });
});

router.delete('/followups/:id', (req, res) => {
  q().prepare("UPDATE followups SET status = 'cancelled' WHERE id = ? AND status = 'pending'").run(req.params.id);
  res.sendStatus(204);
});

router.post('/followups/run', wrap(async (req, res) => {
  res.json({ sent: await runDueFollowups() });
}));

// ---------- Bot ----------
router.get('/bot', (req, res) => {
  res.json({
    settings: db.getSettings(),
    rules: q().prepare('SELECT * FROM bot_rules ORDER BY priority DESC, id').all(),
  });
});

router.put('/bot/settings', (req, res) => {
  for (const k of ['bot_enabled', 'welcome_message', 'fallback_message', 'pause_bot_on_agent_reply']) {
    if (req.body[k] !== undefined) db.setSetting(k, req.body[k]);
  }
  res.json(db.getSettings());
});

const RULE_FIELDS = ['match_type', 'keyword', 'reply', 'add_tag', 'handoff', 'priority', 'enabled'];

router.post('/bot/rules', (req, res) => {
  const r = { match_type: 'contains', reply: '', add_tag: '', handoff: 0, priority: 0, enabled: 1, ...req.body };
  if (!r.keyword) throw new HttpError(400, 'Keyword is required');
  const { lastInsertRowid } = q().prepare(`INSERT INTO bot_rules (${RULE_FIELDS.join(', ')}) VALUES (?, ?, ?, ?, ?, ?, ?)`)
    .run(r.match_type, r.keyword, r.reply, r.add_tag, r.handoff ? 1 : 0, Number(r.priority) || 0, r.enabled ? 1 : 0);
  res.status(201).json(q().prepare('SELECT * FROM bot_rules WHERE id = ?').get(lastInsertRowid));
});

router.patch('/bot/rules/:id', (req, res) => {
  const body = { ...req.body };
  for (const k of ['handoff', 'enabled']) if (body[k] !== undefined) body[k] = body[k] ? 1 : 0;
  patch('bot_rules', req.params.id, body, RULE_FIELDS);
  res.json(must(q().prepare('SELECT * FROM bot_rules WHERE id = ?').get(req.params.id)));
});

router.delete('/bot/rules/:id', (req, res) => {
  q().prepare('DELETE FROM bot_rules WHERE id = ?').run(req.params.id);
  res.sendStatus(204);
});

// ---------- Simulator (test the bot without a real phone) ----------
router.post('/simulate', wrap(async (req, res) => {
  const { phone, name = '', body } = req.body;
  if (!msg.normalizePhone(phone) || !body) throw new HttpError(400, 'Phone and message are required');
  const result = await processInbound({ channel: 'whatsapp', from: phone, name, body, type: 'text', externalId: null });
  res.status(201).json(result);
}));

// JSON errors
router.use((err, req, res, next) => {
  const status = err.status || 500;
  if (status >= 500) console.error('[api]', err);
  res.status(status).json({ error: err.message || 'Server error' });
});

module.exports = router;
