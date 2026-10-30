// Follow-up scheduler: every N seconds, send follow-ups whose time has come.
const db = require('../db');
const { sendMessage, sqlTime } = require('./messages');

let running = false;

async function runDueFollowups(now = new Date()) {
  if (running) return 0; // never overlap two runs
  running = true;
  let sent = 0;
  try {
    const due = db.get().prepare(
      "SELECT * FROM followups WHERE status = 'pending' AND send_at <= ? ORDER BY send_at LIMIT 50"
    ).all(sqlTime(now));

    for (const f of due) {
      // Claim the row first so a crash mid-send can't double-send it
      const claimed = db.get().prepare("UPDATE followups SET status = 'sending' WHERE id = ? AND status = 'pending'").run(f.id);
      if (!claimed.changes) continue;
      try {
        await sendMessage(f.contact_id, f.template_name
          ? { templateName: f.template_name, templateLang: f.template_lang, templateParams: f.template_params.split('\n').map((s) => s.trim()).filter(Boolean) }
          : { body: f.body }, 'followup');
        db.get().prepare("UPDATE followups SET status = 'sent', sent_at = ? WHERE id = ?").run(sqlTime(), f.id);
        sent++;
      } catch (err) {
        db.get().prepare("UPDATE followups SET status = 'failed', error = ? WHERE id = ?").run(err.message, f.id);
      }
    }
  } finally {
    running = false;
  }
  return sent;
}

function start(intervalMs) {
  // A row left in 'sending' means the app stopped mid-send. We can't know whether WhatsApp
  // received it, so mark it failed rather than risk messaging the customer twice.
  db.get().prepare("UPDATE followups SET status = 'failed', error = 'Interrupted while sending - check the chat before retrying' WHERE status = 'sending'").run();
  const timer = setInterval(() => runDueFollowups().catch((e) => console.error('[scheduler]', e)), intervalMs);
  timer.unref();
  return timer;
}

module.exports = { runDueFollowups, start };
