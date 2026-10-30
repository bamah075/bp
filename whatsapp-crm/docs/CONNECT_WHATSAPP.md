# Connect the CRM to the WhatsApp Cloud API (Meta)

This guide takes you from "mock mode" to sending and receiving real WhatsApp messages.
It takes about **30–60 minutes**, plus waiting time for Meta to review your display name and templates.

> Meta renames menu items from time to time. If a button isn't exactly where this guide says,
> look for the same words nearby or search the page. The *order* of the steps stays the same.

---

## What you need before you start

| Item | Why |
|---|---|
| A personal Facebook account | Used to log in to Meta for Developers and Meta Business Suite |
| A **Meta business portfolio** (free, created during setup) | WhatsApp numbers belong to a business |
| A phone number that **can receive an SMS or voice call** | It becomes your business WhatsApp number. It must **not** be registered on WhatsApp right now (see step 7) |
| The CRM running on a **public HTTPS address** | Meta delivers incoming messages to `https://your-domain/webhook` |
| A payment card (for later) | Template messages that *you* start are charged per message. Replies within 24h are free |

---

## Step 1: Put the CRM on a public HTTPS address

Meta's servers must be able to reach your CRM. Choose one:

- **For testing (quickest):** run the CRM on your computer and open a tunnel:
  ```bash
  npm start                    # CRM on http://localhost:3000
  npx ngrok http 3000          # gives you https://xxxx.ngrok-free.app
  ```
  Free ngrok URLs change every restart, so you'd have to update the webhook URL each time.
- **For real use:** deploy to a host such as Render, Railway, Fly.io or a VPS, and keep a fixed URL like `https://crm.yourbusiness.com`.

Write down your URL. We'll call it `YOUR_URL` below.

## Step 2: Create a Meta app

1. Go to **https://developers.facebook.com/apps** and log in.
2. Click **Create app**.
3. When asked for a use case, choose **"Connect with customers through WhatsApp"** (older screens say *Other → Business*).
4. Name the app (e.g. *My Shop CRM*) and pick your **business portfolio**, or create one.
5. Finish. Inside the app, open **WhatsApp → API Setup** (sometimes called *Quickstart* or *Getting started*).

## Step 3: Try the free test number

On the **API Setup** page Meta gives you a **test phone number**. Note these values:

| On the page | Goes into `.env` as |
|---|---|
| **Temporary access token** (click *Generate*) | `WHATSAPP_TOKEN` |
| **Phone number ID** (not the phone number itself!) | `WHATSAPP_PHONE_NUMBER_ID` |
| WhatsApp Business Account ID | (not needed by the CRM; keep it for troubleshooting) |

Then:
1. In the **To** field, add your own mobile number and confirm the code WhatsApp sends you.
   The test number can only *send* to up to 5 numbers you add here.
2. Click **Send message**. You should receive the `hello_world` template on your phone. ✅

## Step 4: Fill in `.env`

```bash
cp .env.example .env
```

Edit `.env`:

```ini
ADMIN_PASSWORD=pick-a-strong-password
WHATSAPP_TOKEN=EAAG...            # from step 3
WHATSAPP_PHONE_NUMBER_ID=1234567890
WHATSAPP_VERIFY_TOKEN=any-random-text-you-choose   # e.g. shop-crm-8f3k2
WHATSAPP_APP_SECRET=abc123...     # App settings → Basic → App secret → Show
GRAPH_API_VERSION=v26.0
```

Restart the CRM. The badge in the top-right corner should now say **● Live**.

> 🔒 Never commit `.env` to Git. It's already in `.gitignore`.

## Step 5: Connect the webhook (incoming messages)

1. In the Meta app, open **WhatsApp → Configuration**.
2. Under **Webhook**, click **Edit**:
   - **Callback URL:** `YOUR_URL/webhook`
   - **Verify token:** exactly the same text as `WHATSAPP_VERIFY_TOKEN`
3. Click **Verify and save**. Meta calls your CRM, and the CRM answers if the tokens match.
4. Under **Webhook fields**, click **Manage** and **Subscribe** to **`messages`**.
   This one field brings both incoming messages *and* delivery receipts (sent / delivered / read).

**Test it:** from your phone, send *"hi, what is the price?"* to the test number.
Within a few seconds it should appear in the CRM **Inbox**, and the bot should reply. 🎉
Try *"你好，请问价格？"* too: the contact is marked as Chinese and the bot answers in Chinese.

## Step 6: Get a permanent access token

The temporary token from step 3 **expires after about 24 hours**. For daily use, create a System User token:

1. Go to **https://business.facebook.com** → **Settings** (Business settings).
2. **Users → System users → Add**. Name it e.g. *crm-bot* and give it the **Admin** role.
3. Select the system user → **Assign assets**:
   - **Apps** → your app → **Full control**
   - **WhatsApp accounts** → your WhatsApp Business account → **Full control**
4. Click **Generate new token** → choose your app → **Token expiration: Never** → tick these permissions:
   - `whatsapp_business_messaging`
   - `whatsapp_business_management`
5. Copy the token into `WHATSAPP_TOKEN` in `.env` and restart. (Meta shows it only once. Store it somewhere safe.)

## Step 7: Add your real business number

The test number is for trying things out. To use your own number:

1. **Make sure the number is not active on WhatsApp.** If it's on the WhatsApp or WhatsApp Business *app*, either:
   - in the app: **Settings → Account → Delete account** (chat history on that phone is lost), **or**
   - keep using the app *and* the API on the same number through a Meta partner that supports **"coexistence"**. That's an extra setup this guide doesn't cover.
2. In the Meta app: **WhatsApp → API Setup → Add phone number** (or in *WhatsApp Manager → Phone numbers → Add*).
3. Enter your **display name** (the business name customers see). Meta reviews it, which usually takes a few hours to a couple of days.
4. Verify the number with the SMS or voice code.
5. Copy the new number's **Phone number ID** into `WHATSAPP_PHONE_NUMBER_ID` and restart.

## Step 8: Business verification and payment

- **Verify your business:** *Business settings → Security Center → Start verification* (business documents required).
  Without it, you can **start** conversations with up to **250 different customers per 24 hours**.
  Verification and good message quality raise that limit. Limits are shared by all numbers in your business portfolio.
  Replying to customers who message you first doesn't count towards this limit.
- **Add a payment method:** *WhatsApp Manager → Payment settings*.

**What costs money (per-message pricing):**

| Message | Cost |
|---|---|
| Free-text replies within 24h of the customer's last message (the bot, your inbox replies) | **Free** |
| *Utility* templates sent while that 24h window is open | **Free** |
| Template messages that start a conversation (marketing / utility / authentication) | Charged per delivered message; the price depends on category and country |

See Meta's current price list: https://developers.facebook.com/docs/whatsapp/pricing

## Step 9: Create message templates in English **and** Chinese

WhatsApp only allows **pre-approved templates** if the customer hasn't messaged you in the last 24 hours.
That matters for follow-ups.

1. Open **WhatsApp Manager → Message templates → Create template**.
2. Pick a **category**:
   - **Utility**: order updates, appointment reminders, follow-ups on a request the customer made
   - **Marketing**: promotions and offers (needs the customer's opt-in)
3. Give it a **name**, e.g. `quote_followup` (lowercase and underscores only).
4. Add the **English (en_US)** version, e.g.:
   `Hi {{1}}, just checking whether you had a chance to look at the quote we sent. Reply here if you have any questions!`
5. Click **Add language → Chinese (CHN) `zh_CN`** and add the Chinese version **under the same name**:
   `{{1}}您好，想跟进一下我们发给您的报价，请问您看过了吗？如有任何问题，欢迎直接回复。`
6. Submit. Approval usually takes minutes to a day.

**Using it in the CRM:** in a follow-up (or *Inbox → Send a template*), type `quote_followup` as the template name,
put `{name}` as the first parameter, and **leave the language empty**. The CRM sends `zh_CN` to Chinese
contacts and `en_US` to everyone else, based on each contact's language.

## Step 10: Go live checklist

- [ ] App switched to **Live** mode (*App settings → Basic*: add a **Privacy Policy URL** and category, then toggle **Live**)
- [ ] Permanent System User token in `.env` (step 6)
- [ ] `WHATSAPP_APP_SECRET` set, so the CRM rejects fake webhook calls
- [ ] Strong `ADMIN_PASSWORD`, and the CRM served over HTTPS
- [ ] Bot welcome and keyword replies reviewed in **both languages** (*Bot* tab)
- [ ] At least one approved follow-up template in `en_US` and `zh_CN`
- [ ] Backups of `data/crm.db` scheduled

---

## Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| **"Verify and save" fails** | The CRM isn't reachable at `YOUR_URL/webhook` over HTTPS, or the verify token doesn't match `.env` *exactly*. Open `YOUR_URL/health` in a browser. It should show `{"ok":true}` |
| Webhook verified but **no messages arrive** | You didn't subscribe to the **`messages`** field (step 5.4). If it's still missing, subscribe the app to your WhatsApp account: `POST https://graph.facebook.com/v26.0/{WABA_ID}/subscribed_apps` with your token |
| CRM log shows **401** on `/webhook` | `WHATSAPP_APP_SECRET` is wrong. Copy it again from *App settings → Basic* |
| Error **190** / "Session has expired" | The temporary token expired. Create the permanent token (step 6) |
| Error **131030** "Recipient not in allowed list" | You're on the test number. Add the recipient in *API Setup → To* (max 5), or switch to your real number |
| Error **131047** "Re-engagement message" | More than 24h since the customer last wrote. Send an approved **template** instead |
| Error **132001** "Template name does not exist in the translation" | The template isn't approved in that language. Add the missing `en_US` / `zh_CN` version (step 9) |
| Phone number stuck as **Pending** | Register it once: `POST https://graph.facebook.com/v26.0/{PHONE_NUMBER_ID}/register` with body `{"messaging_product":"whatsapp","pin":"123456"}` (choose your own 6-digit PIN) |

Official documentation: https://developers.facebook.com/docs/whatsapp/cloud-api
