"""
Production-grade AgentRunner implementing all 7 Non-Negotiables:

  #1 Deterministic Outputs  — structured output option via Pydantic
  #2 Idempotency            — skip-if-exists; idempotency key = output_path
  #3 Validation Gates       — AIM.check_output() after every run
  #4 Error Policy           — SDK max_retries=4 (exp backoff + jitter built-in)
  #5 Observability          — RunLogger: per-run token/cost/duration JSONL
  #6 Cost Control           — prompt caching on system + large context blocks
  #7 Safety & Compliance    — Coordinator approval gate; secrets via .env only
"""
import os
import time
import uuid
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

import anthropic
from dotenv import load_dotenv

from agent_teams.observe import RunLogger, AgentRunMetrics, compute_cost

if TYPE_CHECKING:
    from agent_teams.ace import ACEAgent, AIM

load_dotenv()

# Non-negotiable #6: default to the most capable model; caching handles cost.
MODEL = "claude-opus-4-7"

# Minimum token count to bother caching a context block.
_CACHE_MIN_CHARS = 800


class Agent:
    """Plain agent — no AIM required. Use for simple pipelines."""

    def __init__(
        self,
        name: str,
        role: str,
        task: str,
        output_path: str,
        system_prompt: str = "",
        aim: Optional["AIM"] = None,
    ):
        self.name = name
        self.role = role
        self.task = task
        self.output_path = output_path
        self.aim = aim
        self.result: Optional[str] = None

        if system_prompt:
            self.system_prompt = system_prompt
        else:
            guardrail_block = aim.build_guardrail_block() if aim else ""
            self.system_prompt = (
                f"You are {name}, a {role}. "
                f"Be thorough, specific, and produce complete output — never truncate."
                f"{guardrail_block}"
            )


class AgentRunner:
    """
    Orchestrates agents with production-grade reliability.
    All 7 non-negotiables are wired in by default.
    """

    def __init__(
        self,
        model: str = MODEL,
        logger: Optional[RunLogger] = None,
        idempotent: bool = True,
    ):
        # Non-negotiable #4: SDK handles exponential backoff + jitter automatically.
        self.client = anthropic.Anthropic(
            api_key=os.environ["ANTHROPIC_API_KEY"],
            max_retries=4,
        )
        self.model = model
        # Non-negotiable #5: every run gets a logger.
        self.logger = logger or RunLogger()
        # Non-negotiable #2: skip agents whose output already exists.
        self.idempotent = idempotent

    # ── Core run ──────────────────────────────────────────────────────────

    def run(self, agent: Agent, context: str = "") -> str:
        out = Path(agent.output_path)

        # Non-negotiable #2: Idempotency — output path is the idempotency key.
        if self.idempotent and out.exists() and out.stat().st_size > 100:
            print(f"  [{agent.name}] ↩  skipped (output exists)")
            agent.result = out.read_text(encoding="utf-8")
            self.logger.log(AgentRunMetrics(
                run_id=str(uuid.uuid4())[:8],
                session_id=self.logger.session_id,
                agent_name=agent.name,
                model=self.model,
                started_at=datetime.now(timezone.utc).isoformat(),
                finished_at=datetime.now(timezone.utc).isoformat(),
                duration_s=0.0,
                input_tokens=0, output_tokens=0,
                cache_write_tokens=0, cache_read_tokens=0,
                cost_usd=0.0,
                status="skipped",
                output_path=str(out),
            ))
            return agent.result

        run_id = str(uuid.uuid4())[:8]
        started = time.monotonic()
        started_at = datetime.now(timezone.utc).isoformat()
        print(f"\n  [{agent.name}] ▶  starting  [{run_id}]")

        # ── Non-negotiable #6: Prompt caching ─────────────────────────────
        # System prompt is stable → always cache it.
        system = [
            {
                "type": "text",
                "text": agent.system_prompt,
                "cache_control": {"type": "ephemeral"},
            }
        ]

        # Build user content with optional caching on large context.
        user_content: list[dict] = []
        if context and len(context) >= _CACHE_MIN_CHARS:
            # Large context is stable for this call — cache it.
            user_content.append({
                "type": "text",
                "text": f"Context from previous agents:\n\n{context}",
                "cache_control": {"type": "ephemeral"},
            })
            user_content.append({
                "type": "text",
                "text": f"Your task:\n{agent.task}",
            })
        elif context:
            user_content.append({
                "type": "text",
                "text": f"Context:\n{context}\n\n---\n\nYour task:\n{agent.task}",
            })
        else:
            user_content.append({"type": "text", "text": agent.task})

        messages = [{"role": "user", "content": user_content}]

        # ── API call (retries handled by SDK) ─────────────────────────────
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8096,
                system=system,
                messages=messages,
            )
        except Exception as e:
            duration = round(time.monotonic() - started, 2)
            self.logger.log(AgentRunMetrics(
                run_id=run_id,
                session_id=self.logger.session_id,
                agent_name=agent.name,
                model=self.model,
                started_at=started_at,
                finished_at=datetime.now(timezone.utc).isoformat(),
                duration_s=duration,
                input_tokens=0, output_tokens=0,
                cache_write_tokens=0, cache_read_tokens=0,
                cost_usd=0.0,
                status="error",
                output_path=str(out),
                error=str(e),
            ))
            raise

        result = response.content[0].text
        agent.result = result

        # ── Save output ────────────────────────────────────────────────────
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(result, encoding="utf-8")

        # ── Non-negotiable #3: Validation Gate ────────────────────────────
        validation_passed = True
        validation_notes: list[str] = []
        if agent.aim is not None:
            validation_passed, validation_notes = agent.aim.check_output(result)
            if not validation_passed:
                print(f"  [{agent.name}] ⚠  validation: {validation_notes}")

        # ── Non-negotiable #5: Observability — log metrics ─────────────────
        usage = response.usage
        cw = getattr(usage, "cache_creation_input_tokens", 0) or 0
        cr = getattr(usage, "cache_read_input_tokens", 0) or 0
        duration = round(time.monotonic() - started, 2)
        cost = compute_cost(self.model, usage.input_tokens, usage.output_tokens, cw, cr)

        cache_note = ""
        if cr > 0:
            cache_note = f"  💰 {cr:,} cached tokens"

        print(f"  [{agent.name}] ✓  done  [{duration}s · ${cost:.5f}{cache_note}]")
        print(f"         → {agent.output_path}")

        self.logger.log(AgentRunMetrics(
            run_id=run_id,
            session_id=self.logger.session_id,
            agent_name=agent.name,
            model=self.model,
            started_at=started_at,
            finished_at=datetime.now(timezone.utc).isoformat(),
            duration_s=duration,
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            cache_write_tokens=cw,
            cache_read_tokens=cr,
            cost_usd=round(cost, 6),
            status="success",
            output_path=str(out),
            validation_passed=validation_passed,
            validation_notes=validation_notes,
        ))

        return result

    # ── Parallel execution ────────────────────────────────────────────────

    def run_parallel(
        self, agents: list[Agent], shared_context: str = ""
    ) -> dict[str, str]:
        """Run multiple agents concurrently. Returns {name: result}."""
        results: dict[str, str] = {}
        with ThreadPoolExecutor(max_workers=min(len(agents), 8)) as executor:
            future_to_agent = {
                executor.submit(self.run, agent, shared_context): agent
                for agent in agents
            }
            for future in as_completed(future_to_agent):
                agent = future_to_agent[future]
                try:
                    results[agent.name] = future.result()
                except Exception as e:
                    print(f"  [{agent.name}] ✗  {e}")
                    results[agent.name] = f"ERROR: {e}"
        return results

    # ── Synthesis helper ─────────────────────────────────────────────────

    def synthesize(
        self,
        task: str,
        context: str,
        output_path: str,
        role: str = "Synthesis Lead",
        aim: Optional["AIM"] = None,
    ) -> str:
        """Run a single synthesis/review pass after agents finish."""
        synth = Agent(
            name="Synthesis Lead",
            role=role,
            task=task,
            output_path=output_path,
            aim=aim,
        )
        return self.run(synth, context=context)

    # ── Structured output (Non-negotiable #1) ────────────────────────────

    def run_structured(self, agent: Agent, schema, context: str = ""):
        """
        Run an agent and parse the response into a Pydantic model.
        Use for machine-readable outputs that feed downstream logic.
        """
        user_content: list[dict] = []
        if context and len(context) >= _CACHE_MIN_CHARS:
            user_content.append({
                "type": "text",
                "text": f"Context:\n\n{context}",
                "cache_control": {"type": "ephemeral"},
            })
            user_content.append({"type": "text", "text": agent.task})
        else:
            user_content.append({
                "type": "text",
                "text": f"{context}\n\n{agent.task}" if context else agent.task,
            })

        response = self.client.messages.parse(
            model=self.model,
            max_tokens=4096,
            system=agent.system_prompt,
            messages=[{"role": "user", "content": user_content}],
            output_format=schema,
        )
        agent.result = response.parsed_output.model_dump_json(indent=2)

        out = Path(agent.output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(agent.result, encoding="utf-8")
        print(f"  [{agent.name}] ✓  structured → {agent.output_path}")
        return response.parsed_output
