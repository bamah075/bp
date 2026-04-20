"""
#07 Build a Personal AI Business Assistant
Phase 1: Subagent analyzes OpenClaw repo → Phase 2: 5-agent team builds PA Assistant.
"""
import subprocess
import sys
from agent_teams.core import Agent, AgentRunner

BASE = "outputs/agent_teams_demo/pa_assistant"
REPO_URL = "https://github.com/anthropics/openclawai"


def run(require_approval: bool = True):
    print("\n=== #07 Personal AI Business Assistant ===")
    runner = AgentRunner()

    # ─── Phase 1: Single subagent analyzes reference repo ───
    print("\nPhase 1: Subagent analyzing OpenClaw architecture...")

    repo_analyst = Agent(
        name="Repo Analyst",
        role="software architect and code analyst",
        task=f"""Analyze the OpenClaw AI assistant project from this repo: {REPO_URL}

If you cannot access the repo directly, research OpenClaw / open-source Claude assistant
projects to understand their architecture patterns.

Summarize:
1. Overall architecture and how components connect
2. Key design patterns used (routing, memory, tool use)
3. Technologies and dependencies it relies on
4. The 3 best ideas to borrow for our version
5. The 3 things we should do differently (simpler, more focused for a solo operator)

This analysis will guide the build team.""",
        output_path=f"{BASE}/repo_analysis.md",
    )
    runner.run(repo_analyst)

    if require_approval:
        print(f"\n--- PLAN APPROVAL: Review {BASE}/repo_analysis.md ---")
        print("Press Enter when ready to spawn the build team...")
        input("  > ")

    # ─── Phase 2: Architect designs system first ───
    print("\nPhase 2a: Architect designing system...")

    architect = Agent(
        name="Architect",
        role="senior software architect",
        task=f"""Design the system architecture for "PA Assistant" — a personal AI business
assistant for Prompt Advisers (https://www.promptadvisers.com/).

Based on the repo analysis provided, design:

1. COMPONENT DIAGRAM (text/ASCII)
   Show how: Telegram Bot ↔ Skill Router ↔ Skills ↔ Memory ↔ Claude API

2. API CONTRACTS
   Define the interfaces between components:
   - Message format from Telegram → Router
   - Skill invocation signature: skill_name, input, context → output
   - Memory read/write API

3. TECH STACK
   - Python 3.11+
   - python-telegram-bot for Telegram
   - SQLite for memory (via sqlite3)
   - anthropic SDK for Claude API
   - python-dotenv for config

4. SKILL ROUTER DESIGN
   How it determines which skill to invoke from a plain-text message

5. FILE STRUCTURE
   outputs/agent_teams_demo/pa_assistant/src/
   └── (show the full intended directory tree)

6. WHAT WE BORROW vs WHAT WE BUILD CUSTOM""",
        output_path=f"{BASE}/architecture.md",
    )
    runner.run(architect, context=f"Repo Analysis:\n{repo_analyst.result}")

    if require_approval:
        print(f"\n--- PLAN APPROVAL: Review {BASE}/architecture.md ---")
        print("Press Enter to start the build team...")
        input("  > ")

    arch_context = f"""Repo Analysis:\n{repo_analyst.result}

Architecture Design:\n{architect.result}"""

    # ─── Phase 2b: 4 builders work in parallel ───
    print("\nPhase 2b: Build team working in parallel...")

    telegram_dev = Agent(
        name="Telegram Interface Dev",
        role="Python developer specializing in Telegram bots",
        task=f"""Build the Telegram bot layer for PA Assistant.
Architecture reference provided.

Create complete, working Python code for:
{BASE}/src/telegram_bot/__init__.py — module init
{BASE}/src/telegram_bot/bot.py — Main bot class:
  - Setup with python-telegram-bot
  - Handlers for: text messages, voice notes (transcription placeholder), images, documents
  - Response formatting (markdown, inline keyboards for yes/no confirmations)
  - Conversation thread tracking (group vs DM)
  - start_polling() entry point

Write complete, runnable Python code. Include all imports.
Output the code for each file clearly labeled with its path.""",
        output_path=f"{BASE}/src/telegram_bot/bot.py",
    )

    skills_dev = Agent(
        name="Skill Router Dev",
        role="Python developer specializing in NLP routing and tool systems",
        task=f"""Build the skill router and tools layer for PA Assistant.
Architecture reference provided.

Create complete, working Python code for:
{BASE}/src/skills/__init__.py
{BASE}/src/skills/router.py — SkillRouter class:
  - Skill registry (dict mapping skill names to handlers)
  - Intent detection: analyze message → pick best skill
  - Fallback to Claude general assistant if no skill matches
  - Route method: route(message, context) → (skill_name, result)

{BASE}/src/skills/handlers.py — 8 skill handlers:
  1. draft_email(context) — draft client emails, follow-ups, outreach
  2. content_repurpose(content) — turn transcript/blog into social posts
  3. meeting_prep(context) — summarize context before a consulting call
  4. proposal_writer(brief) — draft project proposals and SOWs
  5. schedule_check(query) — parse and respond to schedule queries
  6. community_pulse(summary) — summarize Skool community activity
  7. invoice_reminder(client_info) — draft payment follow-up messages
  8. research(topic) — use Claude to research and summarize a topic

Each handler uses the Claude API. Include the anthropic import and API calls.
Write complete, runnable Python code with all imports.""",
        output_path=f"{BASE}/src/skills/router.py",
    )

    memory_dev = Agent(
        name="Memory Dev",
        role="Python developer specializing in data persistence and context systems",
        task=f"""Build the memory and context system for PA Assistant.
Architecture reference provided.

Create complete, working Python code for:
{BASE}/src/memory/__init__.py
{BASE}/src/memory/memory.py — MemoryManager class:
  - SQLite backend (creates db on first run)
  - Short-term: store last N messages per conversation thread
  - Long-term: store key-value facts (client names, preferences, project history)
  - Business context: load from business_context.json on startup
  - learn(fact: str) method — parse "remember that X" and store it
  - recall(query: str) method — retrieve relevant facts for a query
  - get_thread(thread_id) / save_message(thread_id, role, content)

{BASE}/src/memory/business_context.json — starter context for Prompt Advisers:
  - Company info, services, pricing, team
  - Frequently used templates
  - Client communication preferences

Write complete, runnable Python code. Include SQL schema and all imports.""",
        output_path=f"{BASE}/src/memory/memory.py",
    )

    integration_dev = Agent(
        name="Integration Dev",
        role="Python developer specializing in system integration and CLI tooling",
        task=f"""Wire everything together for PA Assistant.
Architecture reference provided.

Create complete, working Python code for:

{BASE}/src/main.py — Entry point:
  - Load .env (Telegram token, Claude API key, DB path)
  - Initialize MemoryManager, SkillRouter, TelegramBot
  - Health check on startup: verify Telegram API, Claude API, SQLite
  - Start bot polling
  - Graceful shutdown handler

{BASE}/setup.sh — Setup script:
  #!/bin/bash
  - Install pip dependencies from requirements.txt
  - Create SQLite database
  - Prompt for TELEGRAM_BOT_TOKEN and ANTHROPIC_API_KEY
  - Write .env file
  - Print success message with run instructions

{BASE}/README.md — Setup instructions:
  - How to create a Telegram bot via BotFather
  - Get the token
  - Configure .env
  - Run setup.sh
  - Run python src/main.py

Write complete, runnable code. Include all imports and error handling.""",
        output_path=f"{BASE}/src/main.py",
    )

    builders = [telegram_dev, skills_dev, memory_dev, integration_dev]
    runner.run_parallel(builders, shared_context=arch_context)

    # ─── Phase 3: Test results summary ───
    print("\nPhase 3: Generating test results and run instructions...")

    all_code = "\n\n---\n\n".join(
        f"## {a.name}\n```python\n{a.result}\n```" for a in builders if a.result
    )

    runner.synthesize(
        task="""Write a test results and integration summary document.

Include:
## System Overview
Brief description of what was built and how components connect

## File Structure
Show the complete file tree that was created

## Setup Instructions
```bash
cd outputs/agent_teams_demo/pa_assistant
bash setup.sh
python src/main.py
```

## Test Scenarios
Document 5 test messages to send the bot and expected skill routing:
1. "draft a follow-up email to a client who hasn't responded in 5 days about their AI automation project"
   Expected: → draft_email skill
2. "I have a call with TechCorp tomorrow, help me prep"
   Expected: → meeting_prep skill
[Continue for 3 more examples...]

## Integration Checklist
- [ ] Telegram bot connects and receives messages
- [ ] Skill router correctly identifies intent
- [ ] Memory persists across conversations
- [ ] All 8 skills return useful output
- [ ] Health check passes on startup

## Known Limitations & Next Steps""",
        context=f"Architecture:\n{architect.result}\n\nBuilt components:\n{all_code[:3000]}...",
        output_path=f"{BASE}/test_results.md",
        role="QA Lead / Integration Engineer",
    )

    print(f"\n✓ All outputs saved to {BASE}/")
    print(f"\nTo run the assistant:")
    print(f"  cd {BASE}")
    print(f"  bash setup.sh")
    print(f"  python src/main.py")
