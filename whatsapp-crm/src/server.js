const path = require('node:path');
const crypto = require('node:crypto');
const express = require('express');
const config = require('./config');
const db = require('./db');
const scheduler = require('./services/scheduler');
const { getChannel } = require('./channels');

function basicAuth(req, res, next) {
  if (!config.adminPassword) return next();
  const [scheme, encoded] = (req.get('authorization') || '').split(' ');
  const [user, pass] = Buffer.from(encoded || '', 'base64').toString().split(/:(.*)/s);
  const ok = (a, b) => a.length === b.length && crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b));
  if (scheme === 'Basic' && ok(user || '', config.adminUser) && ok(pass || '', config.adminPassword)) return next();
  res.set('WWW-Authenticate', 'Basic realm="WhatsApp CRM"').status(401).send('Login required');
}

function createApp() {
  const app = express();
  // Keep the raw body: needed to verify Meta's webhook signature
  app.use(express.json({ limit: '1mb', verify: (req, res, buf) => { req.rawBody = buf; } }));

  // Webhook must stay public (Meta calls it); everything else needs a login
  app.use('/webhook', require('./routes/webhook'));
  app.get('/health', (req, res) => res.json({ ok: true }));
  app.use(basicAuth);
  app.use('/api', require('./routes/api'));
  app.use(express.static(path.join(__dirname, '..', 'public')));
  return app;
}

if (require.main === module) {
  db.init();
  scheduler.start(config.schedulerIntervalMs);
  createApp().listen(config.port, () => {
    console.log(`WhatsApp CRM running on http://localhost:${config.port}`);
    console.log(getChannel('whatsapp').isLive()
      ? 'WhatsApp: LIVE (Cloud API)'
      : 'WhatsApp: MOCK mode - set WHATSAPP_TOKEN and WHATSAPP_PHONE_NUMBER_ID in .env to go live');
    if (!config.adminPassword) console.warn('WARNING: ADMIN_PASSWORD is not set - dashboard is open to anyone who can reach it');
    if (!config.whatsapp.appSecret) console.warn('WARNING: WHATSAPP_APP_SECRET is not set - webhook signatures are not verified');
  });
}

module.exports = { createApp };
