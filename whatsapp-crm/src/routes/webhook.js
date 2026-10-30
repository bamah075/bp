// Meta calls these endpoints. Configure the URL https://<your-domain>/webhook in
// Meta Developer Portal > WhatsApp > Configuration, and subscribe to the "messages" field.
const express = require('express');
const config = require('../config');
const { getChannel } = require('../channels');
const { processInbound } = require('../services/bot');
const { updateStatus } = require('../services/messages');

const router = express.Router();

// One-time verification handshake when you save the webhook URL in Meta
router.get('/', (req, res) => {
  if (req.query['hub.mode'] === 'subscribe' && req.query['hub.verify_token'] === config.whatsapp.verifyToken) {
    return res.status(200).send(req.query['hub.challenge']);
  }
  res.sendStatus(403);
});

router.post('/', async (req, res) => {
  const channel = getChannel('whatsapp');
  if (!channel.verifySignature(req.rawBody, req.get('x-hub-signature-256'))) {
    return res.sendStatus(401);
  }
  // Answer Meta quickly (it retries slow webhooks), then do the work
  res.sendStatus(200);

  const { messages, statuses } = channel.parseWebhook(req.body);
  for (const s of statuses) updateStatus(s);
  for (const m of messages) {
    try {
      await processInbound(m);
    } catch (err) {
      console.error('[webhook] failed to process message', m.externalId, err.message);
    }
  }
});

module.exports = router;
