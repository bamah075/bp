"""
Non-negotiable #5: Observability
Trace every agent run end-to-end — token usage, cost, duration, status.
Persist evidence as JSONL artifacts so failures are reproducible.
"""
import json
import time
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Per-model pricing ($/token) as of 2026
_PRICING: dict[str, dict[str, float]] = {
    "claude-opus-4-7": {
        "input": 5.00 / 1_000_000,
        "output": 25.00 / 1_000_000,
        "cache_write": 6.25 / 1_000_000,   # 1.25x input
        "cache_read": 0.50 / 1_000_000,    # 0.1x input
    },
    "claude-sonnet-4-6": {
        "input": 3.00 / 1_000_000,
        "output": 15.00 / 1_000_000,
        "cache_write": 3.75 / 1_000_000,
        "cache_read": 0.30 / 1_000_000,
    },
    "claude-haiku-4-5": {
        "input": 1.00 / 1_000_000,
        "output": 5.00 / 1_000_000,
        "cache_write": 1.25 / 1_000_000,
        "cache_read": 0.10 / 1_000_000,
    },
}


def compute_cost(model: str, input_tokens: int, output_tokens: int,
                 cache_write_tokens: int = 0, cache_read_tokens: int = 0) -> float:
    p = _PRICING.get(model, _PRICING["claude-opus-4-7"])
    return (
        input_tokens * p["input"]
        + output_tokens * p["output"]
        + cache_write_tokens * p["cache_write"]
        + cache_read_tokens * p["cache_read"]
    )


@dataclass
class AgentRunMetrics:
    run_id: str
    session_id: str
    agent_name: str
    model: str
    started_at: str
    finished_at: str
    duration_s: float
    input_tokens: int
    output_tokens: int
    cache_write_tokens: int
    cache_read_tokens: int
    cost_usd: float
    status: str          # success | error | skipped
    output_path: str
    validation_passed: bool = True
    validation_notes: list[str] = field(default_factory=list)
    error: Optional[str] = None


class RunLogger:
    """Persist every agent run to a JSONL audit log. Non-negotiable #5."""

    def __init__(self, log_dir: str = "outputs/logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.session_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"run_{self.session_id}.jsonl"
        self.runs: list[AgentRunMetrics] = []

    def log(self, metrics: AgentRunMetrics) -> None:
        self.runs.append(metrics)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(metrics)) + "\n")

    def summary(self) -> dict:
        success = sum(1 for r in self.runs if r.status == "success")
        skipped = sum(1 for r in self.runs if r.status == "skipped")
        errors = sum(1 for r in self.runs if r.status == "error")
        total_cost = sum(r.cost_usd for r in self.runs)
        total_duration = sum(r.duration_s for r in self.runs)
        cache_savings = sum(
            r.cache_read_tokens * _PRICING.get(r.model, _PRICING["claude-opus-4-7"])["input"]
            * (1 - 0.1)   # savings vs full price
            for r in self.runs
        )
        return {
            "session_id": self.session_id,
            "total_agents": len(self.runs),
            "success": success,
            "skipped": skipped,
            "errors": errors,
            "total_cost_usd": round(total_cost, 5),
            "cache_savings_usd": round(cache_savings, 5),
            "total_duration_s": round(total_duration, 1),
            "log_file": str(self.log_file),
        }

    def print_summary(self) -> None:
        s = self.summary()
        print(f"\n{'─'*52}")
        print(f"  Run Summary  [{s['session_id']}]")
        print(f"  Agents : {s['total_agents']}  "
              f"({s['success']} ok · {s['skipped']} skipped · {s['errors']} errors)")
        print(f"  Cost   : ${s['total_cost_usd']:.5f}  "
              f"(saved ${s['cache_savings_usd']:.5f} via cache)")
        print(f"  Time   : {s['total_duration_s']}s")
        print(f"  Log    : {s['log_file']}")
        print(f"{'─'*52}")
