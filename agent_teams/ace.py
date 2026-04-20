"""
The ACE Framework — Aim · Coordinate · Execute

AIM       The "What"  — Intent, acceptance tests, guardrails, process steps.
COORDINATE The "Who & When" — ReAct loop with approval-level routing.
EXECUTE   The "How"  — Deterministic, testable, single-purpose tools.

References the 7 Non-Negotiables for Production-Ready AI Agents:
  #1 Deterministic Outputs   — acceptance tests + schema validation
  #2 Idempotency             — skip-if-exists in AgentRunner.run()
  #3 Validation Gates        — AIM.check_output() before marking done
  #4 Error Policy            — handled in AgentRunner via SDK max_retries
  #5 Observability           — RunLogger in observe.py
  #6 Cost Control            — prompt caching in AgentRunner
  #7 Safety & Compliance     — ApprovalLevel routing + guardrails in AIM
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ── Approval levels (COORDINATE layer) ────────────────────────────────────
class ApprovalLevel(Enum):
    AUTO    = "auto"     # reads, local ops — execute without asking
    ASK     = "ask"      # writes, new tools — pause and confirm
    REQUIRE = "require"  # legal, PII — hard block until explicit approval


# ── AIM layer ──────────────────────────────────────────────────────────────
@dataclass
class AIM:
    """
    The 'What' — Intent & Blueprint for a single agent.
    Human-authored SOP that makes the agent's purpose testable.
    """
    goal: str                           # one-sentence outcome
    inputs: dict[str, str]              # {param_name: description}
    acceptance_tests: list[str]         # Given-When-Then or keyword checks
    guardrails: list[str]               # binary stop conditions (never violate)
    process_steps: list[str]            # ordered execution plan
    approval_level: ApprovalLevel = ApprovalLevel.AUTO

    def build_guardrail_block(self) -> str:
        if not self.guardrails:
            return ""
        rules = "\n".join(f"  • {g}" for g in self.guardrails)
        return f"\n\nHARD GUARDRAILS — never violate these rules:\n{rules}"

    def check_output(self, text: str) -> tuple[bool, list[str]]:
        """
        Non-negotiable #3: Validation Gate.
        Run acceptance tests against the agent's output.
        Returns (passed, list_of_failures).
        """
        failures: list[str] = []
        for test in self.acceptance_tests:
            if test.startswith("min_words:"):
                min_w = int(test.split(":")[1].strip())
                actual = len(text.split())
                if actual < min_w:
                    failures.append(f"Word count too low: {actual} < {min_w}")

            elif test.startswith("contains:"):
                keyword = test.split(":", 1)[1].strip().lower()
                if keyword not in text.lower():
                    failures.append(f"Missing required content: '{keyword}'")

            elif test.startswith("not_contains:"):
                keyword = test.split(":", 1)[1].strip().lower()
                if keyword in text.lower():
                    failures.append(f"Forbidden content found: '{keyword}'")

            elif test.startswith("min_sections:"):
                min_s = int(test.split(":")[1].strip())
                sections = text.count("##")
                if sections < min_s:
                    failures.append(f"Too few sections: {sections} < {min_s}")

        return len(failures) == 0, failures


# ── ACEAgent — Agent enriched with AIM ────────────────────────────────────
@dataclass
class ACEAgent:
    """
    Agent with a full AIM blueprint attached.
    The system prompt is automatically augmented with guardrails from AIM.
    """
    name: str
    role: str
    task: str
    output_path: str
    aim: AIM
    system_prompt: str = ""
    result: Optional[str] = None

    def __post_init__(self):
        guardrail_block = self.aim.build_guardrail_block()
        if not self.system_prompt:
            self.system_prompt = (
                f"You are {self.name}, a {self.role}. "
                f"Your goal: {self.aim.goal}\n\n"
                f"Be thorough and specific. Never truncate output — write the full result."
                f"{guardrail_block}"
            )

    def validate(self) -> tuple[bool, list[str]]:
        if not self.result:
            return False, ["No output produced"]
        return self.aim.check_output(self.result)


# ── Coordinator — ReAct loop with approval routing ─────────────────────────
class Coordinator:
    """
    Non-negotiable #7: Safety & Compliance.
    Routes agent actions through the correct approval tier before execution.
    """

    @staticmethod
    def gate(agent: ACEAgent, action_description: str = "") -> bool:
        """
        Returns True if the action may proceed.
        AUTO  → always proceed
        ASK   → print prompt and wait for user input
        REQUIRE → print prompt, require explicit 'yes' to continue
        """
        level = agent.aim.approval_level

        if level == ApprovalLevel.AUTO:
            return True

        print(f"\n  ⚠  Approval required [{level.value.upper()}] for [{agent.name}]")
        if action_description:
            print(f"     Action: {action_description}")

        if level == ApprovalLevel.ASK:
            resp = input("  Proceed? [Enter to approve / 'n' to skip]: ").strip().lower()
            return resp != "n"

        if level == ApprovalLevel.REQUIRE:
            resp = input("  Type 'yes' to approve: ").strip().lower()
            return resp == "yes"

        return False


# ── Pre-built AIM blueprints for each team ─────────────────────────────────
AIMS: dict[str, AIM] = {

    "blog_writer": AIM(
        goal="Transform a video transcript into a 1,200-word first-person blog post",
        inputs={"transcript": "full video transcript text"},
        acceptance_tests=[
            "min_words:1000",
            "contains:##",
            "contains:CTA",
        ],
        guardrails=[
            "Never copy the transcript verbatim — transform it into blog prose",
            "Write in first person",
            "Include at least 3 subheadings",
        ],
        process_steps=[
            "Identify 3 compelling insights from the transcript",
            "Write a hook paragraph",
            "Develop 3-5 subheadings with key insights",
            "Write conclusion with CTA",
        ],
    ),

    "researcher": AIM(
        goal="Find 8-10 data points with sources for a pitch deck research brief",
        inputs={"topic": "research topic"},
        acceptance_tests=[
            "min_words:400",
            "min_sections:4",
            "contains:source",
        ],
        guardrails=[
            "Every data point must include a source",
            "No fabricated statistics — mark uncertain data as [ESTIMATED]",
        ],
        process_steps=[
            "Research the topic using available knowledge",
            "Collect 8-10 specific stats with sources",
            "Explain why each data point matters",
        ],
    ),

    "rfp_analyst": AIM(
        goal="Extract all requirements, evaluation criteria, and submission rules from an RFP",
        inputs={"rfp_url": "URL or text of the RFP document"},
        acceptance_tests=[
            "min_words:300",
            "contains:requirement",
            "contains:evaluation",
        ],
        guardrails=[
            "Never invent requirements not in the source document",
            "Flag any ambiguous requirements with [CLARIFICATION NEEDED]",
        ],
        process_steps=[
            "Read the full RFP",
            "Extract numbered requirements",
            "Extract evaluation criteria and weights",
            "Extract submission rules",
            "List ambiguities",
        ],
    ),

    "synthesis_lead": AIM(
        goal="Synthesize multiple agent outputs into a coherent executive brief or report",
        inputs={"agent_outputs": "collected results from all team members"},
        acceptance_tests=[
            "min_words:300",
            "contains:recommendation",
        ],
        guardrails=[
            "Base all claims on the provided agent outputs — no outside invention",
            "Flag contradictions between agents rather than silently choosing one",
        ],
        process_steps=[
            "Read all agent outputs",
            "Identify common themes and conflicts",
            "Synthesize into a structured report",
            "Make a clear recommendation",
        ],
    ),

    "devils_advocate": AIM(
        goal="Challenge every assumption and find the risks nobody wants to talk about",
        inputs={"team_analyses": "analyses from all other board members"},
        acceptance_tests=[
            "min_words:400",
            "min_sections:3",
        ],
        guardrails=[
            "Be honest even if the answer is uncomfortable",
            "Back every risk claim with a concrete scenario, not vague worry",
        ],
        process_steps=[
            "Read all other analyses",
            "Identify the 3 most optimistic assumptions",
            "Challenge each with evidence or counter-scenarios",
            "Surface 3 risks nobody else raised",
        ],
        approval_level=ApprovalLevel.AUTO,
    ),
}
