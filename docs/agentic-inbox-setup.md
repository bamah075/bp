# Agentic Inbox

Source: https://github.com/cloudflare/agentic-inbox

## What it is

An email client where an AI agent reads your inbox and drafts replies (you
always confirm before anything sends). Runs entirely on Cloudflare Workers.

- Replaces Superhuman / other AI email assistants (~$30/mo)
- Officially open-sourced by Cloudflare
- Each mailbox lives in its own isolated Durable Object
- Uses Cloudflare's own AI (Workers AI), so your email never leaves your account

## Architecture

- **Frontend**: React single-page app with an AI agent control panel
- **API/routing**: Hono worker handling HTTP requests and server-side rendering
- **Backend**: Mailbox Durable Objects (SQLite-backed), Email Agent Durable
  Objects (run the AI operations), and R2 storage for attachments
- Browser <-> Worker communication happens over WebSockets, with the worker
  routing requests to the right Durable Object

## How to start

1. One-click **Deploy to Cloudflare Workers** from the repo.
2. Complete the post-deploy setup:
   - **Configure Cloudflare Access**: enable one-click Access on the deployed
     Worker, then copy the `POLICY_AUD` and `TEAM_DOMAIN` values into the
     Worker's secrets. This is mandatory in production — without it, the
     inbox is publicly exposed.
   - **Set up Email Routing**: in your domain's Email Routing settings,
     create a catch-all rule that forwards to the deployed Worker.
   - **Enable the email service**: configure the `send_email` binding so the
     Worker can send outbound messages.
   - **Create a mailbox**: open the deployed app and create a mailbox for
     the address you want the agent to manage.
