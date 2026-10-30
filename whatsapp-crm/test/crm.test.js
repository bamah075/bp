// End-to-end tests against an in-memory database, in mock WhatsApp mode.
process.env.DB_PATH = ':memory:';
process.env.ADMIN_PASSWORD = '';
process.env.WHATSAPP_TOKEN = '';
process.env.WHATSAPP_APP_SECRET = 'test-secret';
process.env.WHATSAPP_VERIFY_TOKEN = 'verify-me';

const test = require('node:test');
const assert = require('node:assert');
const crypto = require('node:crypto');
const db = require('../src/db');
const { createApp } = require('../src/server');
const { runDueFollowups } = require('../src/services/scheduler');

db.init(':memory:');
let base;
const server = createApp().listen(0);
test.before(() => { base = `http://localhost:${server.address().port}`; });
test.after(() => server.close());

async function call(path, method = 'GET', body) {
  const res = await fetch(base + path, { method, headers: { 'Content-Type': 'application/json' }, body: body && JSON.stringify(body) });
  return { status: res.status, data: res.status === 204 ? null : await res.json().catch(() => null) };
}

function webhookPayload(from, name, text, id) {
  return {
    object: 'whatsapp_business_account',
    entry: [{ changes: [{ value: {
      contacts: [{ wa_id: from, profile: { name } }],
      messages: [{ from, id, type: 'text', text: { body: text } }],
    } }] }],
  };
}

async function postWebhook(payload, secret = 'test-secret') {
  const raw = JSON.stringify(payload);
  const sig = 'sha256=' + crypto.createHmac('sha256', secret).update(raw).digest('hex');
  const res = await fetch(base + '/webhook', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Hub-Signature-256': sig }, body: raw });
  await new Promise((r) => setTimeout(r, 50)); // processing happens after the 200 response
  return res.status;
}

test('webhook verification handshake', async () => {
  const ok = await fetch(`${base}/webhook?hub.mode=subscribe&hub.verify_token=verify-me&hub.challenge=123`);
  assert.equal(await ok.text(), '123');
  const bad = await fetch(`${base}/webhook?hub.mode=subscribe&hub.verify_token=wrong&hub.challenge=123`);
  assert.equal(bad.status, 403);
});

test('rejects webhooks with a bad signature', async () => {
  assert.equal(await postWebhook(webhookPayload('111', 'X', 'hi', 'w0'), 'wrong-secret'), 401);
});

test('inbound message creates contact, bot welcomes + answers keyword, duplicates ignored', async () => {
  assert.equal(await postWebhook(webhookPayload('6591234567', 'Alice Tan', 'What is the price?', 'wamid.1')), 200);
  await postWebhook(webhookPayload('6591234567', 'Alice Tan', 'What is the price?', 'wamid.1')); // Meta retry

  const { data: contacts } = await call('/api/contacts?q=Alice');
  assert.equal(contacts.length, 1);
  const alice = contacts[0];
  assert.equal(alice.phone, '6591234567');
  assert.ok(alice.tags.includes('interested-pricing'));
  assert.equal(alice.in_window, true);

  const { data: msgs } = await call(`/api/contacts/${alice.id}/messages`);
  assert.deepEqual(msgs.map((m) => [m.direction, m.sent_by]), [['in', null], ['out', 'bot'], ['out', 'bot']]);
  assert.match(msgs[1].body, /Hi Alice Tan/); // welcome personalised
  assert.match(msgs[2].body, /\$99/);
});

test('handoff rule pauses the bot; agent reply also pauses it', async () => {
  let r = await call('/api/simulate', 'POST', { phone: '+1 555 000 1111', name: 'Bob', body: 'hello' });
  const bob = r.data.contact;
  r = await call('/api/simulate', 'POST', { phone: '15550001111', body: 'AGENT' });
  assert.equal(r.data.contact.bot_paused, 1);
  assert.ok(r.data.contact.tags.includes('needs-human'));

  await call(`/api/contacts/${bob.id}`, 'PATCH', { bot_paused: false });
  const sent = await call(`/api/contacts/${bob.id}/messages`, 'POST', { body: 'Hi {name}, how can I help?' });
  assert.equal(sent.status, 201);
  assert.equal(sent.data.body, 'Hi Bob, how can I help?');
  assert.equal((await call(`/api/contacts/${bob.id}`)).data.bot_paused, 1);
});

test('follow-ups: send when due, cancel on reply, schedule by tag', async () => {
  const { data: [alice] } = await call('/api/contacts?q=Alice');
  await call('/api/followups', 'POST', { contactId: alice.id, body: 'Following up, {first_name}!', delayMinutes: 0 });
  await call('/api/followups', 'POST', { contactId: alice.id, body: 'Later one', delayMinutes: 60 });
  assert.equal(await runDueFollowups(), 1);

  const { data: msgs } = await call(`/api/contacts/${alice.id}/messages`);
  assert.equal(msgs.at(-1).body, 'Following up, Alice!');
  assert.equal(msgs.at(-1).sent_by, 'followup');

  await postWebhook(webhookPayload('6591234567', 'Alice Tan', 'thanks!', 'wamid.2'));
  const { data: fus } = await call(`/api/followups?contactId=${alice.id}`);
  assert.deepEqual(fus.map((f) => f.status).sort(), ['cancelled', 'sent']);

  const byTag = await call('/api/followups', 'POST', { tag: 'needs-human', body: 'Hi!', delayMinutes: 5 });
  assert.equal(byTag.data.scheduled, 1);
});

test('delivery status receipts update messages without downgrading', async () => {
  const { data: [alice] } = await call('/api/contacts?q=Alice');
  const { data: m } = await call(`/api/contacts/${alice.id}/messages`, 'POST', { body: 'status test' });
  const status = (s) => ({ object: 'whatsapp_business_account', entry: [{ changes: [{ value: { statuses: [{ id: m.external_id, status: s }] } }] }] });
  await postWebhook(status('read'));
  await postWebhook(status('delivered'));
  const { data: msgs } = await call(`/api/contacts/${alice.id}/messages`);
  assert.equal(msgs.find((x) => x.id === m.id).status, 'read');
});

test('pipeline: stages and deals', async () => {
  const { data: stages } = await call('/api/stages');
  assert.equal(stages[0].name, 'New Lead');
  const { data: [alice] } = await call('/api/contacts?q=Alice');
  const { data: deal } = await call('/api/deals', 'POST', { title: 'Website package', value: 1200, contact_id: alice.id });
  assert.equal(deal.stage_id, stages[0].id);
  const won = stages.find((s) => s.name === 'Won');
  await call(`/api/deals/${deal.id}`, 'PATCH', { stage_id: won.id });
  const { data: status } = await call('/api/status');
  assert.equal(status.stats.wonValue, 1200);
  assert.equal((await call(`/api/stages/${won.id}`, 'DELETE')).status, 409); // has deals
});

test('contacts CSV export', async () => {
  const res = await fetch(base + '/api/contacts/export.csv');
  const text = await res.text();
  assert.match(text, /^name,phone,email/);
  assert.match(text, /"Alice Tan","6591234567","","en"/);
});

test('multi-language: Chinese contact is detected and the bot replies in Chinese', async () => {
  const { data } = await call('/api/simulate', 'POST', { phone: '8613800138000', name: '王伟', body: '你好，请问价格是多少？' });
  const wang = data.contact;
  assert.equal(wang.language, 'zh');
  assert.ok(wang.tags.includes('interested-pricing'));
  const { data: msgs } = await call(`/api/contacts/${wang.id}/messages`);
  assert.match(msgs[1].body, /^您好 王伟/);     // Chinese welcome
  assert.match(msgs[2].body, /套餐每月/);       // Chinese "price" rule, not the English one
  assert.equal(msgs.length, 3);

  // English-only rules don't fire for a Chinese contact
  await call('/api/simulate', 'POST', { phone: '8613800138000', body: 'hours' });
  const { data: after } = await call(`/api/contacts/${wang.id}/messages`);
  assert.equal(after.length, 4);

  // Staff can override the language; unknown codes are rejected
  assert.equal((await call(`/api/contacts/${wang.id}`, 'PATCH', { language: 'xx' })).status, 400);
});

test('multi-language: follow-ups send the version for the contact\'s language; templates pick zh_CN', async () => {
  const { data: [wang] } = await call('/api/contacts?q=8613800138000');
  const { data: [alice] } = await call('/api/contacts?q=Alice');
  await call('/api/contacts/' + alice.id, 'PATCH', { tags: 'promo' });
  await call('/api/contacts/' + wang.id, 'PATCH', { tags: 'promo', bot_paused: false });
  await call('/api/followups', 'POST', { tag: 'promo', body: 'Promo ends Friday, {first_name}!', translations: { zh: '{name}，优惠周五结束！' }, delayMinutes: 0, cancelOnReply: false });
  assert.equal(await runDueFollowups(), 2);
  const last = async (id) => (await call(`/api/contacts/${id}/messages`)).data.at(-1).body;
  assert.equal(await last(wang.id), '王伟，优惠周五结束！');
  assert.equal(await last(alice.id), 'Promo ends Friday, Alice!');

  const wa = require('../src/channels/whatsapp');
  const original = wa.sendTemplate;
  let usedLang;
  wa.sendTemplate = async (to, name, lang) => { usedLang = lang; return { externalId: 'tpl-1' }; };
  try {
    await call(`/api/contacts/${wang.id}/messages`, 'POST', { templateName: 'order_update' });
    assert.equal(usedLang, 'zh_CN');
  } finally {
    wa.sendTemplate = original;
  }
});

test('multi-language: an existing database from before this feature is upgraded', () => {
  const { DatabaseSync } = require('node:sqlite');
  const os = require('node:os');
  const path = require('node:path');
  const file = path.join(os.tmpdir(), `crm-migrate-${process.pid}.db`);
  const old = new DatabaseSync(file);
  old.exec(`CREATE TABLE contacts (id INTEGER PRIMARY KEY, name TEXT NOT NULL DEFAULT '', phone TEXT NOT NULL UNIQUE, email TEXT NOT NULL DEFAULT '',
    tags TEXT NOT NULL DEFAULT '', notes TEXT NOT NULL DEFAULT '', source TEXT NOT NULL DEFAULT 'whatsapp', social TEXT NOT NULL DEFAULT '{}',
    bot_paused INTEGER NOT NULL DEFAULT 0, unread INTEGER NOT NULL DEFAULT 0, last_inbound_at TEXT, last_message_at TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')), updated_at TEXT NOT NULL DEFAULT (datetime('now')));
    INSERT INTO contacts (phone, name) VALUES ('123', 'Old');`);
  old.close();
  const upgraded = db.init(file);
  try {
    assert.equal(upgraded.prepare('SELECT language FROM contacts').get().language, '');
    assert.ok(upgraded.prepare('PRAGMA table_info(bot_rules)').all().some((c) => c.name === 'language'));
  } finally {
    upgraded.close();
    for (const f of [file, `${file}-wal`, `${file}-shm`]) require('node:fs').rmSync(f, { force: true });
    db.init(':memory:');
  }
});
