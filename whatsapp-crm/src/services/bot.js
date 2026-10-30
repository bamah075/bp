// Keyword auto-reply bot. Runs on every inbound message.
//   1. New contact            -> welcome message
//   2. Matching keyword rule  -> rule reply (+ optional tag / human handoff)
//   3. Nothing matched        -> fallback message (if set)
// Messages are picked in the contact's language; rules can be limited to one language.
// The bot stays silent while a contact is "paused" (a human has taken over).
const db = require('../db');
const { DEFAULT_LANGUAGE, localizedSetting } = require('../i18n');
const { sendMessage, addTag, getContact, recordInbound } = require('./messages');

function findRule(text, lang = DEFAULT_LANGUAGE) {
  const t = String(text || '').trim().toLowerCase();
  if (!t) return null;
  const rules = db.get().prepare(
    "SELECT * FROM bot_rules WHERE enabled = 1 AND (language = '' OR language = ?) ORDER BY priority DESC, id ASC"
  ).all(lang);
  return rules.find((r) => {
    const k = r.keyword.trim().toLowerCase();
    if (!k) return false;
    if (r.match_type === 'exact') return t === k;
    // "contains" matches whole words, so "price" matches "what's the price?" but not "priceless".
    // Chinese has no spaces between words, so CJK keywords match anywhere in the message.
    if (/[^\x00-\x7f]/.test(k)) return t.includes(k);
    return new RegExp(`(^|\\W)${k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}($|\\W)`, 'i').test(t);
  }) || null;
}

async function handleInbound({ contact, isNew, text }) {
  const settings = db.getSettings();
  if (settings.bot_enabled !== '1' || contact.bot_paused) return [];

  const replies = [];
  const send = async (body) => {
    if (body && body.trim()) replies.push(await sendMessage(contact.id, { body }, 'bot'));
  };

  const lang = contact.language || DEFAULT_LANGUAGE;
  const rule = findRule(text, lang);
  if (isNew) await send(localizedSetting(settings, 'welcome_message', lang));

  if (rule) {
    await send(rule.reply);
    if (rule.add_tag) addTag(contact.id, rule.add_tag);
    if (rule.handoff) db.get().prepare('UPDATE contacts SET bot_paused = 1 WHERE id = ?').run(contact.id);
  } else if (!isNew) {
    await send(localizedSetting(settings, 'fallback_message', lang));
  }
  return replies;
}

// Process an inbound message end to end: store it, then let the bot respond.
async function processInbound(normalized) {
  const saved = recordInbound(normalized);
  if (!saved) return null; // duplicate webhook delivery
  try {
    await handleInbound({ contact: saved.contact, isNew: saved.isNew, text: normalized.body });
  } catch (err) {
    console.error('[bot] reply failed:', err.message);
  }
  return { ...saved, contact: getContact(saved.contact.id) };
}

module.exports = { findRule, handleInbound, processInbound };
