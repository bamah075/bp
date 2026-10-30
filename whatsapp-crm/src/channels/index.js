// Channel registry. To add Instagram / Messenger / Telegram later, create an
// adapter with the same interface as whatsapp.js and register it here.
const whatsapp = require('./whatsapp');

const channels = { whatsapp };

function getChannel(name = 'whatsapp') {
  const ch = channels[name];
  if (!ch) throw new Error(`Unknown channel: ${name}`);
  return ch;
}

module.exports = { getChannel, channels };
