// WhatsApp Cloud API adapter (official Meta API).
// Docs: https://developers.facebook.com/docs/whatsapp/cloud-api
//
// Every channel adapter exposes the same shape so the CRM core never needs
// to know which platform a message came from:
//   name, isLive(), sendText(), sendTemplate(), parseWebhook(), verifySignature()
const crypto = require('node:crypto');
const config = require('../config');

const wa = config.whatsapp;

function isLive() {
  return Boolean(wa.token && wa.phoneNumberId);
}

async function callGraph(payload) {
  if (!isLive()) {
    // Mock mode: pretend it was sent so the whole CRM can be tested without Meta credentials.
    console.log('[whatsapp:mock] would send', JSON.stringify(payload));
    return { externalId: `mock-${crypto.randomUUID()}` };
  }
  const res = await fetch(`https://graph.facebook.com/${wa.graphVersion}/${wa.phoneNumberId}/messages`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${wa.token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ messaging_product: 'whatsapp', ...payload }),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = data.error || {};
    // 131047 = more than 24h since the customer's last message: only templates are allowed
    const hint = err.code === 131047 ? ' (outside the 24h window — use an approved template)' : '';
    throw new Error(`${err.message || `HTTP ${res.status}`}${hint}`);
  }
  return { externalId: data.messages?.[0]?.id || null };
}

function sendText(to, body) {
  return callGraph({ to, type: 'text', text: { body, preview_url: true } });
}

function sendTemplate(to, name, lang = 'en_US', params = []) {
  const template = { name, language: { code: lang } };
  if (params.length) {
    template.components = [{ type: 'body', parameters: params.map((text) => ({ type: 'text', text })) }];
  }
  return callGraph({ to, type: 'template', template });
}

// Pull the readable text out of the different inbound message types
function extractText(m) {
  switch (m.type) {
    case 'text': return m.text?.body || '';
    case 'button': return m.button?.text || '';
    case 'interactive': return m.interactive?.button_reply?.title || m.interactive?.list_reply?.title || '';
    case 'location': return `📍 Location: ${m.location?.latitude}, ${m.location?.longitude}`;
    default: return m[m.type]?.caption || `[${m.type}]`;
  }
}

// Normalise Meta's nested webhook payload into flat lists the CRM understands
function parseWebhook(payload) {
  const messages = [];
  const statuses = [];
  if (payload?.object !== 'whatsapp_business_account') return { messages, statuses };

  for (const entry of payload.entry || []) {
    for (const change of entry.changes || []) {
      const value = change.value || {};
      const names = Object.fromEntries((value.contacts || []).map((c) => [c.wa_id, c.profile?.name || '']));
      for (const m of value.messages || []) {
        messages.push({
          channel: 'whatsapp',
          from: m.from,
          name: names[m.from] || '',
          externalId: m.id,
          type: m.type,
          body: extractText(m),
        });
      }
      for (const s of value.statuses || []) {
        statuses.push({ externalId: s.id, status: s.status, error: s.errors?.[0]?.title || null });
      }
    }
  }
  return { messages, statuses };
}

// Meta signs each webhook with HMAC-SHA256 of the raw body using your App Secret.
function verifySignature(rawBody, header) {
  if (!wa.appSecret) return true; // not configured (dev) — server logs a warning at startup
  if (!header || !rawBody) return false;
  const expected = 'sha256=' + crypto.createHmac('sha256', wa.appSecret).update(rawBody).digest('hex');
  const a = Buffer.from(expected);
  const b = Buffer.from(header);
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}

module.exports = { name: 'whatsapp', isLive, sendText, sendTemplate, parseWebhook, verifySignature };
