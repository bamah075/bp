"""
#04 Competitive Intelligence Report
4 analysts research 4 competitors in parallel → Synthesis Lead → Intelligence Report.
"""
from agent_teams.core import Agent, AgentRunner

BASE = "outputs/agent_teams_demo/competitive_intel"

PRODUCT = "Claude Code — the AI-powered coding assistant CLI from Anthropic"
COMPETITORS = ["Cursor", "Codex (OpenAI)", "GitHub Copilot", "Windsurf (Codeium)"]


def run(product: str = PRODUCT, competitors: list[str] = None):
    print("\n=== #04 Competitive Intelligence Report ===")
    runner = AgentRunner()

    if competitors is None:
        competitors = COMPETITORS

    ANALYSIS_TEMPLATE = """Analyze {competitor} as a competitor to {product}.

Document (using the latest information available as of 2026):

## Product Overview & Core Features
## Pricing Model and Tiers
## Target Audience and Positioning
## Strengths (what they do better than Claude Code)
## Weaknesses (where Claude Code has an advantage)
## Recent News, Funding, or Product Launches (2025-2026)
## Top 3 Surprising Findings

Be specific and factual. Include pricing numbers, feature names, and concrete comparisons."""

    analysts = [
        Agent(
            name=f"{comp.split(' ')[0]} Analyst",
            role="competitive intelligence researcher",
            task=ANALYSIS_TEMPLATE.format(competitor=comp, product=product),
            output_path=f"{BASE}/{comp.lower().replace(' ', '_').replace('(', '').replace(')', '')}_analysis.md",
        )
        for comp in competitors
    ]

    print(f"\nPhase 1: {len(analysts)} analysts researching in parallel...")
    runner.run_parallel(analysts)

    # Each analyst shares top 3 findings before synthesis
    top_findings = "\n\n".join(
        f"### {a.name} — Top 3 Surprising Findings\n"
        + "\n".join(
            line for line in (a.result or "").split("\n")
            if "surprising" in line.lower() or "##" in line or line.startswith("-")
        )[:600]
        for a in analysts
        if a.result
    )

    all_analyses = "\n\n---\n\n".join(
        f"## {a.name}\n{a.result}" for a in analysts if a.result
    )

    print("\nPhase 2: Synthesis Lead building battlecard report...")
    runner.synthesize(
        task=f"""Using all 4 competitor analyses, create a comprehensive competitive intelligence report for {product}.

Structure:
## Executive Summary (3-4 sentences, key takeaway)
## Competitive Landscape Overview (positioning map narrative)
## Head-to-Head Comparison Table
| Feature | Claude Code | Cursor | Codex | GitHub Copilot | Windsurf |
(Fill in: Pricing, IDE Integration, Agent Mode, Model, Offline Support, Team Features)

## Where Claude Code Wins
## Where Competitors Have the Edge
## Key Battlecard (top 5 objections and responses)
## Strategic Recommendations (3-5 actions for Claude Code team)
## Top Surprising Findings Across All Analysts

Be opinionated and specific. This is an internal strategy document.""",
        context=f"TOP FINDINGS SHARED BY ANALYSTS:\n{top_findings}\n\nFULL ANALYSES:\n{all_analyses}",
        output_path=f"{BASE}/intelligence_report.md",
        role="Competitive Intelligence Lead",
    )

    print(f"\n✓ All outputs saved to {BASE}/")
