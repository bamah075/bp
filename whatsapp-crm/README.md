# 💬 WhatsApp CRM

A self-hosted CRM built on the **official WhatsApp Cloud API**. It gives you:

| Feature | What it does |
|---|---|
| **Shared inbox** | Read and reply to WhatsApp chats from the browser. Delivery ticks (sent / delivered / read) and unread counts are shown. |
| **Contacts** | Every new WhatsApp sender is saved automatically. Add names, email, tags, notes and social handles. Search, filter by tag, export to CSV. |
| **Follow-ups** | Schedule messages for later, for one contact or everyone with a tag. They can **cancel automatically if the customer replies first**. Templates are supported for chats older than 24h. |
| **Sales pipeline** | Kanban board with drag-and-drop deals, custom stages and colours, plus pipeline value totals. |
| **WhatsApp bot** | Welcome message, keyword auto-replies, auto-tagging, fallback reply, and **human handoff**: the bot pauses for a contact when you take over. |
| **Ready for social media** | Every message records its channel, and contacts store Instagram / Facebook / TikTok handles. New channels plug into `src/channels/`. |

---

## 1. Quick start (5 minutes, no WhatsApp account needed)

Requirements: **Node.js 22.13 or newer** (uses the built-in SQLite, so there is no database to install).

```bash
cd whatsapp-crm
npm install
cp .env.example .env        # then set ADMIN_PASSWORD
npm start
```

Open http://localhost:3000 and log in with `ADMIN_USER` / `ADMIN_PASSWORD`.

With no WhatsApp token set, the app runs in **mock mode**: outgoing messages are printed to the console instead of being sent. Go to **Settings → Simulator** and send a fake incoming message such as `Hi, what is the price?`. You'll see:

1. A new contact created in **Contacts**
2. The bot's welcome message plus the "price" keyword reply in **Inbox**
3. The tag `interested-pricing` added automatically

Run the tests with `npm test`.

## 2. Connect real WhatsApp

1. Go to https://developers.facebook.com/apps → **Create app** → type **Business** → add the **WhatsApp** product.
2. Under **WhatsApp → API Setup**, copy into `.env`:
   - **Phone number ID** → `WHATSAPP_PHONE_NUMBER_ID`
   - **Access token** → `WHATSAPP_TOKEN` (the temporary token expires in 24h. For production, create a **System User** token in Business Settings.)
3. **App settings → Basic → App secret** → `WHATSAPP_APP_SECRET` (used to verify that webhooks really come from Meta).
4. Make the app reachable over public HTTPS. Deploy it (Render, Railway, Fly.io, a VPS…) or use a tunnel for testing: `ngrok http 3000`.
5. **WhatsApp → Configuration → Webhook**:
   - Callback URL: `https://YOUR-DOMAIN/webhook`
   - Verify token: the value of `WHATSAPP_VERIFY_TOKEN`
   - Click **Verify and save**, then **subscribe to the `messages` field**.
6. Restart the app. The badge in the top right should say **● Live**.

### WhatsApp rules you need to know

- **24-hour window**: you can send free-text messages only within 24h of the customer's last message. After that, WhatsApp only accepts **pre-approved templates** (create them in WhatsApp Manager). The inbox warns you when a chat is outside the window, and follow-ups can use a template instead of text.
- **Opt-in**: only message people who have agreed to hear from you. Spammy numbers get blocked by Meta.
- The test phone number Meta gives you can only message numbers you've added as recipients in API Setup.

## 3. How it works

```
WhatsApp user ──► Meta Cloud API ──► POST /webhook ──► save contact + message ──► bot decides reply
                                                                                       │
Browser dashboard ◄──► /api/* (Express) ◄──► SQLite (data/crm.db)                       ▼
                                   ▲                                         Meta Cloud API ──► user
          follow-up scheduler ─────┘ (checks every 30s for due follow-ups)
```

```
src/
  server.js            Express app, login, startup
  config.js            Reads .env
  db.js                SQLite schema + default stages / bot rules
  channels/
    whatsapp.js        Send messages, parse webhooks, verify signatures (Cloud API)
    index.js           Channel registry: add Instagram/Messenger here later
  services/
    messages.js        Contacts, inbound/outbound messages, 24h window, delivery status
    bot.js             Keyword bot + human handoff
    scheduler.js       Sends due follow-ups
  routes/
    webhook.js         Endpoints Meta calls
    api.js             JSON API for the dashboard
public/                Dashboard (plain HTML/CSS/JS, no build step)
test/                  End-to-end tests (node --test)
```

### Bot logic

1. Bot switched off, or paused for this contact → do nothing.
2. First message from a new contact → send the **welcome message**.
3. Highest-priority matching **keyword rule** → send its reply, add its tag, and pause the bot if it's a **handoff** rule (e.g. "AGENT").
4. No match → send the **fallback message** (empty by default = stay silent).

When you reply to a contact yourself, the bot pauses for that contact (configurable), so it never talks over you. Re-enable it with the 🤖 toggle in the chat header.

### Follow-ups

- Each follow-up is stored with a send time. The scheduler sends anything due every `SCHEDULER_INTERVAL_SECONDS`.
- **Cancel on reply** (on by default): if the contact messages you before the follow-up goes out, it is cancelled automatically, so you don't nag someone who already answered.
- **Schedule by tag**: e.g. follow up with everyone tagged `interested-pricing`.

## 4. Adding social media channels later

Instagram DMs and Facebook Messenger use the **same Meta webhook system** as WhatsApp, so they are the natural next step:

1. Create `src/channels/instagram.js` with the same functions as `whatsapp.js` (`sendText`, `parseWebhook`, `verifySignature`, `isLive`). Instagram webhooks arrive with `object: "instagram"`, and you send through the `/me/messages` Graph endpoint.
2. Register it in `src/channels/index.js`.
3. Route `object: "instagram"` payloads to it in `routes/webhook.js`.
4. Match contacts on the `social` field (already in the database) so one person's WhatsApp and Instagram chats appear together.

TikTok, Telegram and X (Twitter) can follow the same adapter pattern.

## 5. Going to production: checklist

- [ ] Set a strong `ADMIN_PASSWORD` and serve over HTTPS
- [ ] Set `WHATSAPP_APP_SECRET` (otherwise webhook signatures are not checked)
- [ ] Use a permanent System User token, not the 24h test token
- [ ] Back up `data/crm.db` regularly (it's a single file)
- [ ] Run with a process manager (`pm2 start npm -- start`) or in Docker

## Ideas for next steps

- AI replies (e.g. Claude) when no keyword rule matches
- Multiple team members with their own logins and assigned chats
- Media messages (images, documents, voice notes)
- CSV contact import and broadcast campaigns with approved templates
- Instagram / Messenger channels (see section 4)
