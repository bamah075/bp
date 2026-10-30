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
  assert.match(text, /"Alice Tan","6591234567"/);
});
