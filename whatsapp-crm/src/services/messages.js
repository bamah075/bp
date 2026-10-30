// Core messaging logic shared by the webhook, the dashboard, the bot and the scheduler.
const db = require('../db');
const { getChannel } = require('../channels');
const { detectLanguage, templateLanguage } = require('../i18n');

const WINDOW_MS = 24 * 60 * 60 * 1000;

const normalizePhone = (p) => String(p || '').replace(/\D/g, '');
const sqlTime = (d = new Date()) => d.toISOString().replace('T', ' ').slice(0, 19);
const parseSqlTime = (s) => (s ? new Date(s.replace(' ', 'T') + 'Z') : null);

function getContact(id) {
  return db.get().prepare('SELECT * FROM contacts WHERE id = ?').get(id);
}

function personalize(text, contact) {
  const name = contact?.name || 'there';
  return String(text || '')
    .replaceAll('{name}', name)
    .replaceAll('{first_name}', name.split(' ')[0]);
}

// WhatsApp only allows free-form messages within 24h of the customer's last message.
function inServiceWindow(contact) {
  const last = parseSqlTime(contact?.last_inbound_at);
  return Boolean(last && Date.now() - last.getTime() < WINDOW_MS);
}

function addTag(contactId, tag) {
  tag = String(tag || '').trim();
  if (!tag) return;
  const c = getContact(contactId);
  const tags = new Set(c.tags.split(',').map((t) => t.trim()).filter(Boolean));
  tags.add(tag);
  db.get().prepare("UPDATE contacts SET tags = ?, updated_at = datetime('now') WHERE id = ?").run([...tags].join(','), contactId);
}

function upsertContact({ phone, name = '', source = 'whatsapp' }) {
  phone = normalizePhone(phone);
  if (!phone) throw new Error('Phone number is required');
  const d = db.get();
  const existing = d.prepare('SELECT * FROM contacts WHERE phone = ?').get(phone);
  if (existing) {
    if (name && !existing.name) d.prepare('UPDATE contacts SET name = ? WHERE id = ?').run(name, existing.id);
    return { contact: getContact(existing.id), isNew: false };
  }
  const { lastInsertRowid } = d.prepare('INSERT INTO contacts (phone, name, source) VALUES (?, ?, ?)').run(phone, name, source);
  return { contact: getContact(lastInsertRowid), isNew: true };
}

// Save an inbound message (from the webhook or the simulator). Returns null for duplicates,
// because Meta can retry the same webhook more than once.
function recordInbound({ channel = 'whatsapp', from, name, externalId, type = 'text', body }) {
  const d = db.get();
  if (externalId && d.prepare('SELECT 1 FROM messages WHERE external_id = ?').get(externalId)) return null;

  const { contact, isNew } = upsertContact({ phone: from, name, source: channel });
  const now = sqlTime();
  const { lastInsertRowid } = d.prepare(
    `INSERT INTO messages (contact_id, channel, direction, body, type, status, external_id, created_at)
     VALUES (?, ?, 'in', ?, ?, 'received', ?, ?)`
  ).run(contact.id, channel, body, type, externalId || null, now);

  d.prepare('UPDATE contacts SET unread = unread + 1, last_inbound_at = ?, last_message_at = ? WHERE id = ?')
    .run(now, now, contact.id);

  // Remember the customer's language from their first message we can recognise.
  // Staff can change it on the contact; we never overwrite a language that is already set.
  const detected = !contact.language && detectLanguage(body);
  if (detected) d.prepare('UPDATE contacts SET language = ? WHERE id = ?').run(detected, contact.id);

  // The customer replied, so cancel follow-ups that were waiting for "no reply"
  d.prepare(
    `UPDATE followups SET status = 'cancelled', error = 'Contact replied'
     WHERE contact_id = ? AND status = 'pending' AND cancel_on_reply = 1`
  ).run(contact.id);

  return { contact: getContact(contact.id), isNew, messageId: Number(lastInsertRowid) };
}

// Send a message to a contact. `content` is { body } or { templateName, templateLang, templateParams[] }.
async function sendMessage(contactId, content, sentBy = 'agent') {
  const d = db.get();
  const contact = getContact(contactId);
  if (!contact) throw new Error('Contact not found');

  const isTemplate = Boolean(content.templateName);
  const body = isTemplate
    ? `[template: ${content.templateName}] ${(content.templateParams || []).join(' | ')}`.trim()
    : personalize(content.body, contact);
  if (!isTemplate && !body.trim()) throw new Error('Message is empty');

  const now = sqlTime();
  const { lastInsertRowid } = d.prepare(
    `INSERT INTO messages (contact_id, channel, direction, body, type, status, sent_by, created_at)
     VALUES (?, 'whatsapp', 'out', ?, ?, 'queued', ?, ?)`
  ).run(contact.id, body, isTemplate ? 'template' : 'text', sentBy, now);
  const id = Number(lastInsertRowid);

  try {
    const channel = getChannel('whatsapp');
    const { externalId } = isTemplate
      ? await channel.sendTemplate(contact.phone, content.templateName, content.templateLang || templateLanguage(contact.language),
          (content.templateParams || []).map((p) => personalize(p, contact)))
      : await channel.sendText(contact.phone, body);
    d.prepare("UPDATE messages SET status = 'sent', external_id = ? WHERE id = ?").run(externalId, id);
  } catch (err) {
    d.prepare("UPDATE messages SET status = 'failed', error = ? WHERE id = ?").run(err.message, id);
    throw Object.assign(err, { messageId: id });
  } finally {
    d.prepare('UPDATE contacts SET last_message_at = ? WHERE id = ?').run(now, contact.id);
  }

  // A human replied: stop the bot for this contact so it doesn't talk over them
  if (sentBy === 'agent' && db.getSettings().pause_bot_on_agent_reply === '1') {
    d.prepare('UPDATE contacts SET bot_paused = 1 WHERE id = ?').run(contact.id);
  }
  return d.prepare('SELECT * FROM messages WHERE id = ?').get(id);
}

const STATUS_RANK = { queued: 0, sent: 1, delivered: 2, read: 3 };

// Delivery receipts from WhatsApp. Never downgrade (receipts can arrive out of order).
function updateStatus({ externalId, status, error }) {
  const d = db.get();
  const msg = d.prepare('SELECT id, status FROM messages WHERE external_id = ?').get(externalId);
  if (!msg) return;
  if (status === 'failed') {
    d.prepare("UPDATE messages SET status = 'failed', error = ? WHERE id = ?").run(error || 'Delivery failed', msg.id);
  } else if ((STATUS_RANK[status] ?? -1) > (STATUS_RANK[msg.status] ?? -1)) {
    d.prepare('UPDATE messages SET status = ? WHERE id = ?').run(status, msg.id);
  }
}

module.exports = {
  normalizePhone, sqlTime, parseSqlTime, personalize, inServiceWindow,
  getContact, upsertContact, addTag, recordInbound, sendMessage, updateStatus,
};
