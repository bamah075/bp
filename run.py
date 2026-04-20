#!/usr/bin/env python3
"""
Agent Teams — CLI entry point
ACE Framework + 7 Non-Negotiables for Production-Ready AI Agents

Usage:
  python run.py <team_number> [options]

Non-negotiables enforced on every run:
  #1 Deterministic Outputs  — Pydantic schemas for structured outputs
  #2 Idempotency            — --no-cache flag to force re-run
  #3 Validation Gates       — AIM acceptance tests after each agent
  #4 Error Policy           — SDK max_retries=4 with exp backoff + jitter
  #5 Observability          — JSONL audit log in outputs/logs/
  #6 Cost Control           — Prompt caching on system + context blocks
  #7 Safety & Compliance    — ApprovalLevel gates; secrets via .env only
"""
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description="Run an Agent Team with the ACE Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Teams:
  1  Content Repurposing Pipeline   — 1 transcript → 4 platform pieces (parallel)
  2  Pitch Deck Builder             — Research → Slides → .pptx (sequential)
  3  RFP Response Generator         — Parallel analysis → full proposal
  4  Competitive Intelligence       — 4 analysts → synthesis battlecard
  5  Advisory Board Decision        — 5 agents debate → GO/NO-GO brief
  6  Marketing Campaign Launch      — Email + Social + Ads + Landing Page
  7  Personal AI Business Assistant — Telegram bot with skill routing + memory

ACE Folder Structure:
  /aims/        Human-authored SOPs and acceptance tests (the "What")
  /agent_teams/ Coordinator + AgentRunner (the "Who & When")
  /execution/   Single-purpose deterministic tools (the "How")
  /outputs/     All agent outputs, audit logs, and artifacts
  /tmp/         Scratch space (never committed)
        """,
    )
    parser.add_argument("team", type=int, choices=range(1, 8), help="Team number (1-7)")
    parser.add_argument("--transcript", default="transcript.md",
                        help="[Team 1] Path to transcript .md file")
    parser.add_argument("--rfp-url", default=None,
                        help="[Team 3] Override default RFP URL")
    parser.add_argument("--no-cache", action="store_true",
                        help="Disable idempotency — re-run all agents even if outputs exist")
    parser.add_argument("--no-approval", action="store_true",
                        help="[Teams 2,7] Skip plan-approval gates")
    parser.add_argument("--model", default=None,
                        help="Override model (default: claude-opus-4-7)")

    args = parser.parse_args()

    # Patch idempotency / model into AgentRunner defaults if needed
    if args.no_cache or args.model:
        import agent_teams.core as core_module
        if args.no_cache:
            core_module.AgentRunner.__init__.__defaults__  # exists; patch via kwargs below
        if args.model:
            core_module.MODEL = args.model

    require_approval = not args.no_approval
    idempotent = not args.no_cache

    # Pass idempotent flag to each team via a monkey-patch on AgentRunner's default
    # (teams import AgentRunner and instantiate it without args)
    import agent_teams.core as core
    _orig_init = core.AgentRunner.__init__

    def _patched_init(self, model=core.MODEL, logger=None, idempotent=idempotent):
        _orig_init(self, model=model, logger=logger, idempotent=idempotent)

    core.AgentRunner.__init__ = _patched_init

    if args.team == 1:
        if not Path(args.transcript).exists():
            print(f"Creating sample transcript at {args.transcript}...")
            Path(args.transcript).write_text(
                "# Sample Transcript\n\n"
                "This is a sample transcript. Replace with your actual content.\n\n"
                "Key point 1: AI agents are transforming how teams work...\n"
                "Key point 2: The shift from single models to multi-agent systems...\n"
                "Key point 3: Practical patterns for building agent teams today...\n"
                "Key point 4: The ACE Framework — Aim, Coordinate, Execute...\n"
                "Key point 5: Why reliability engineering principles apply to AI agents..."
            )
        from agent_teams.teams.t01_content_repurposing import run
        runner = run(transcript_path=args.transcript)

    elif args.team == 2:
        from agent_teams.teams.t02_pitch_deck_builder import run
        run(require_approval=require_approval)

    elif args.team == 3:
        from agent_teams.teams.t03_rfp_response import run
        kwargs = {}
        if args.rfp_url:
            kwargs["rfp_url"] = args.rfp_url
        run(**kwargs)

    elif args.team == 4:
        from agent_teams.teams.t04_competitive_intel import run
        run()

    elif args.team == 5:
        from agent_teams.teams.t05_advisory_board import run
        run()

    elif args.team == 6:
        from agent_teams.teams.t06_marketing_campaign import run
        run()

    elif args.team == 7:
        from agent_teams.teams.t07_pa_assistant import run
        run(require_approval=require_approval)


if __name__ == "__main__":
    main()
