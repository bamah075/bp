const fs = require('node:fs');
const path = require('node:path');
const { DatabaseSync } = require('node:sqlite');
const config = require('./config');

let db;

const SCHEMA = `
CREATE TABLE IF NOT EXISTS contacts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL DEFAULT '',
  phone TEXT NOT NULL UNIQUE,          -- digits only, international format (e.g. 6591234567)
  email TEXT NOT NULL DEFAULT '',
  tags TEXT NOT NULL DEFAULT '',       -- comma separated
  notes TEXT NOT NULL DEFAULT '',
  source TEXT NOT NULL DEFAULT 'whatsapp',
  social TEXT NOT NULL DEFAULT '{}',   -- JSON: { instagram, facebook, tiktok, ... } for future channels
  bot_paused INTEGER NOT NULL DEFAULT 0,
  language TEXT NOT NULL DEFAULT '',   -- '' = not detected yet; otherwise a code from src/i18n.js
  unread INTEGER NOT NULL DEFAULT 0,
  last_inbound_at TEXT,
  last_message_at TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
  channel TEXT NOT NULL DEFAULT 'whatsapp',
  direction TEXT NOT NULL CHECK (direction IN ('in','out')),
  body TEXT NOT NULL DEFAULT '',
  type TEXT NOT NULL DEFAULT 'text',
  status TEXT NOT NULL DEFAULT 'received', -- received | queued | sent | delivered | read | failed
  error TEXT,
  external_id TEXT,
  sent_by TEXT,                            -- agent | bot | followup (outbound only)
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_messages_contact ON messages(contact_id, id);
CREATE INDEX IF NOT EXISTS idx_messages_external ON messages(external_id);

CREATE TABLE IF NOT EXISTS stages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  position INTEGER NOT NULL DEFAULT 0,
  color TEXT NOT NULL DEFAULT '#64748b'
);

CREATE TABLE IF NOT EXISTS deals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  contact_id INTEGER REFERENCES contacts(id) ON DELETE SET NULL,
  stage_id INTEGER REFERENCES stages(id) ON DELETE SET NULL,
  title TEXT NOT NULL,
  value REAL NOT NULL DEFAULT 0,
  notes TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS followups (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
  body TEXT NOT NULL DEFAULT '',
  template_name TEXT NOT NULL DEFAULT '',   -- approved WhatsApp template (needed outside the 24h window)
  template_lang TEXT NOT NULL DEFAULT '',   -- '' = pick from the contact's language
  template_params TEXT NOT NULL DEFAULT '', -- one body parameter per line, supports {name}
  translations TEXT NOT NULL DEFAULT '{}',  -- JSON { zh: '...' }: per-language versions of body
  send_at TEXT NOT NULL,                    -- UTC 'YYYY-MM-DD HH:MM:SS'
  cancel_on_reply INTEGER NOT NULL DEFAULT 1,
  status TEXT NOT NULL DEFAULT 'pending',   -- pending | sent | failed | cancelled
  error TEXT,
  sent_at TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_followups_due ON followups(status, send_at);

CREATE TABLE IF NOT EXISTS bot_rules (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  match_type TEXT NOT NULL DEFAULT 'contains', -- exact | contains
  keyword TEXT NOT NULL,
  reply TEXT NOT NULL DEFAULT '',
  add_tag TEXT NOT NULL DEFAULT '',
  handoff INTEGER NOT NULL DEFAULT 0,          -- 1 = pause bot so a human takes over
  language TEXT NOT NULL DEFAULT '',           -- '' = any language, else only for contacts in that language
  priority INTEGER NOT NULL DEFAULT 0,
  enabled INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS settings (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
`;

const DEFAULT_SETTINGS = {
  bot_enabled: '1',
  welcome_message: 'Hi {name}! 👋 Thanks for messaging us. Reply *PRICE* for pricing, *HOURS* for opening hours, or *AGENT* to talk to a person.',
  fallback_message: '',
  welcome_message_zh: '您好 {name}！👋 感谢您的留言。回复 *价格* 了解价格，回复 *营业时间* 了解营业时间，或回复 *人工* 联系客服。',
  fallback_message_zh: '',
  pause_bot_on_agent_reply: '1',
};

// Columns added after the first release. CREATE TABLE IF NOT EXISTS won't add them to an
// existing database, so add any that are missing.
const MIGRATIONS = [
  ['contacts', 'language', "TEXT NOT NULL DEFAULT ''"],
  ['followups', 'translations', "TEXT NOT NULL DEFAULT '{}'"],
  ['bot_rules', 'language', "TEXT NOT NULL DEFAULT ''"],
];

function migrate() {
  for (const [table, column, type] of MIGRATIONS) {
    const exists = db.prepare(`PRAGMA table_info(${table})`).all().some((c) => c.name === column);
    if (!exists) db.exec(`ALTER TABLE ${table} ADD COLUMN ${column} ${type}`);
  }
}

function seed() {
  if (db.prepare('SELECT COUNT(*) AS n FROM stages').get().n === 0) {
    const ins = db.prepare('INSERT INTO stages (name, position, color) VALUES (?, ?, ?)');
    [['New Lead', '#3b82f6'], ['Contacted', '#8b5cf6'], ['Proposal', '#f59e0b'], ['Won', '#22c55e'], ['Lost', '#ef4444']]
      .forEach(([name, color], i) => ins.run(name, i, color));
  }
  if (db.prepare('SELECT COUNT(*) AS n FROM bot_rules').get().n === 0) {
    const ins = db.prepare('INSERT INTO bot_rules (match_type, keyword, reply, add_tag, handoff, priority, language) VALUES (?, ?, ?, ?, ?, ?, ?)');
    ins.run('contains', 'price', 'Our packages start from $99/month. Want a quote? Reply *AGENT* and a team member will help.', 'interested-pricing', 0, 10, 'en');
    ins.run('contains', 'hours', 'We are open Mon–Fri, 9am–6pm.', '', 0, 5, 'en');
    ins.run('exact', 'agent', 'Sure! A team member will reply shortly. 🙌', 'needs-human', 1, 20, 'en');
    ins.run('contains', '价格', '我们的套餐每月 $99 起。需要报价吗？回复 *人工*，我们的团队成员会为您服务。', 'interested-pricing', 0, 10, 'zh');
    ins.run('contains', '营业时间', '我们的营业时间为周一至周五，上午9点至下午6点。', '', 0, 5, 'zh');
    ins.run('exact', '人工', '好的！客服人员会尽快回复您。🙌', 'needs-human', 1, 20, 'zh');
  }
  const insSetting = db.prepare('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)');
  for (const [k, v] of Object.entries(DEFAULT_SETTINGS)) insSetting.run(k, v);
}

function init(dbPath = config.dbPath) {
  if (dbPath !== ':memory:') fs.mkdirSync(path.dirname(dbPath), { recursive: true });
  db = new DatabaseSync(dbPath);
  db.exec('PRAGMA journal_mode = WAL; PRAGMA foreign_keys = ON;');
  db.exec(SCHEMA);
  migrate();
  seed();
  return db;
}

function get() {
  if (!db) init();
  return db;
}

function getSettings() {
  const rows = get().prepare('SELECT key, value FROM settings').all();
  return Object.fromEntries(rows.map((r) => [r.key, r.value]));
}

function setSetting(key, value) {
  get().prepare('INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value')
    .run(key, String(value));
}

module.exports = { init, get, getSettings, setSetting };
