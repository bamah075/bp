# #07 Build a Personal AI Business Assistant

**Use case:** Subagent analysis → Agent team build. A working Telegram bot with skill routing, memory, and business context.

---

Create an agent team to build a personal AI business assistant — a better, customized version of OpenClaw built specifically to run my company, Prompt Advisers (https://www.promptadvisers.com/).

**The end goal:** a working CLI I can start with a single command that connects to Telegram, understands my business context, picks the right tool for any task, and helps me run my company day-to-day.

---

**Step 1 (Subagent):** Clone https://github.com/anthropics/openclawai and read through the codebase. Summarize:
- The overall architecture and how components connect
- Key design patterns used
- What technologies and dependencies it relies on
- The 3 best ideas we should steal for our version
- The 3 things we should do differently (simpler, more focused)

Save the analysis to outputs/agent_teams_demo/pa_assistant/repo_analysis.md.

---

**Step 2 (Agent Team):** Using insights from the subagent's analysis, spawn 5 teammates to build our custom version. Require plan approval from each before they start coding.

1. **Architect** — Design the system architecture for "PA Assistant":
   - Component diagram showing how all pieces connect
   - API contracts between components
   - Tech stack: Python, python-telegram-bot, SQLite for memory, Claude API
   - A skill router that picks the best skill for any incoming request
   - File structure and module boundaries
   
   Save to outputs/agent_teams_demo/pa_assistant/architecture.md. **This must complete and be approved before other teammates begin.**

2. **Telegram Interface** — Build the Telegram bot layer:
   - Bot setup with python-telegram-bot library
   - Message handler for text, voice notes (transcribed), images, documents
   - Response formatting (markdown, inline keyboards for confirmations)
   - Conversation thread tracking (group vs DM context)
   - Own all files in outputs/agent_teams_demo/pa_assistant/src/telegram_bot/

3. **Skill Router and Tools** — Build the intelligence layer:
   - Skill registry with 8 skills for running Prompt Advisers:
     - `draft-email` — draft client emails, follow-ups, outreach
     - `content-repurpose` — turn transcript/blog into social posts
     - `meeting-prep` — summarize context before a consulting call
     - `proposal-writer` — draft project proposals and SOWs
     - `schedule-check` — query Google Calendar availability
     - `community-pulse` — summarize recent Skool community activity
     - `invoice-reminder` — draft payment follow-up messages
     - `research` — web search and summarize findings on a topic
   - Intent detection routing incoming messages to the right skill
   - Own all files in outputs/agent_teams_demo/pa_assistant/src/skills/

4. **Memory and Context** — Build the business context system:
   - Short-term memory (current conversation thread)
   - Long-term memory (client names, project history, preferences)
   - Business context file loaded on startup (company info, services, pricing, team)
   - SQLite storage with retrieval API
   - A "learn" command: "remember that Client X prefers async updates" → stored
   - Own all files in outputs/agent_teams_demo/pa_assistant/src/memory/

5. **Integration and CLI** — Wire everything together:
   - Single entry point: `python main.py`
   - Setup script: `setup.sh` — installs deps, creates SQLite db, prompts for API keys
   - Health check on startup: verify Telegram, Claude API, database
   - README.md with clear setup instructions
   - Own outputs/agent_teams_demo/pa_assistant/src/main.py, setup.sh, README.md

After all teammates finish:
- Run the full test suite
- Print exact commands to start the assistant
- Do a live test: send the bot "draft a follow-up email to a client who hasn't responded in 5 days about their AI automation project" and verify it routes correctly
- Document result in outputs/agent_teams_demo/pa_assistant/test_results.md
