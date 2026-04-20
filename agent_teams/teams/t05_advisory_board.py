"""
#05 Advisory Board Decision Analysis
5 agents debate a high-stakes business decision → GO/NO-GO/CONDITIONAL recommendation.
"""
from agent_teams.core import Agent, AgentRunner

BASE = "outputs/agent_teams_demo/big_problem"

DECISION = """Should we launch a $7,500 live 6-week AI Leadership Bootcamp for executives
and CEOs who want to manage AI teams and integrate AI into their operations —
or should we start with a $2,000 self-paced course first to validate demand?"""

CONTEXT = """We run Prompt Advisers (https://www.promptadvisers.com/), an AI consulting
and education company. We already have a free Skool community with 800+ members.
Our audience is a mix of solopreneurs, agency owners, and mid-level managers —
but we want to go upmarket to C-suite executives.
The bootcamp would cover: building an AI strategy, managing AI-augmented teams,
evaluating AI tools for enterprise, and measuring ROI on AI initiatives."""


def run(decision: str = DECISION, context: str = CONTEXT):
    print("\n=== #05 Advisory Board Decision Analysis ===")
    runner = AgentRunner()

    board_context = f"DECISION QUESTION:\n{decision}\n\nBUSINESS CONTEXT:\n{context}"

    # Phase 1: All 5 board members research independently in parallel
    print("\nPhase 1: Advisory board members doing independent research (parallel)...")

    market_researcher = Agent(
        name="Market Researcher",
        role="market research analyst specializing in executive education",
        task=f"""{board_context}

Analyze the executive AI education market:
- Who's selling high-ticket AI programs to C-suite? What do they charge?
- What formats work best (live cohort vs self-paced vs hybrid)?
- Typical completion rates and satisfaction metrics
- What executives actually want to learn vs what vendors sell
- Total addressable market estimate with rough numbers
- Is there a gap in the current market Prompt Advisers could fill?""",
        output_path=f"{BASE}/market_research.md",
    )

    audience_analyst = Agent(
        name="Audience Gap Analyst",
        role="audience strategy and brand positioning consultant",
        task=f"""{board_context}

Investigate the gap between current audience (solopreneurs, agency owners) and target (executives/CEOs):
- What marketing channels actually reach C-suite?
- What credibility signals do executives need before spending $7,500?
- How different is the sales cycle? (Length, decision makers, procurement)
- What would need to change about brand positioning and website?
- What's the risk of alienating the existing community by going upmarket?
- Give a realistic timeline for the audience transition""",
        output_path=f"{BASE}/audience_analysis.md",
    )

    financial_modeler = Agent(
        name="Financial Modeler",
        role="financial analyst and business model expert",
        task=f"""{board_context}

Build a rough financial model comparing both scenarios:

SCENARIO A: $7,500 bootcamp (15 seats per cohort, live delivery, 6 weeks)
SCENARIO B: $2,000 self-paced course (unlimited seats, async)

For each scenario calculate:
- Build costs (time + tools + production)
- Revenue per cohort/launch
- Profit margin
- Break-even point (# of students)
- Time to first dollar
- 12-month revenue projection (realistic and optimistic cases)
- Key financial risks

Format as a comparison table where possible.""",
        output_path=f"{BASE}/financial_model.md",
    )

    competitive_strategist = Agent(
        name="Competitive Strategist",
        role="competitive strategy and market positioning expert",
        task=f"""{board_context}

Map who's already selling executive AI education:
- Maven cohort courses (who's selling, what they charge, how many seats)
- University executive programs (Wharton, Harvard, MIT — pricing, positioning)
- Consulting firm workshops (McKinsey, Deloitte, boutiques)
- Reforge and similar platforms
- YouTube creators who've gone upmarket

For each competitor: pricing, cohort size, positioning, how they'd view Prompt Advisers.
Identify the specific positioning gap that universities and big firms CAN'T fill.
Where does a creator-led, practitioner-focused brand have a genuine advantage?""",
        output_path=f"{BASE}/competitive_strategy.md",
    )

    devils_advocate = Agent(
        name="Devil's Advocate",
        role="critical risk analyst and contrarian thinker",
        task=f"""{board_context}

Your job: find every reason this could fail. Be brutally honest.

Challenge these assumptions:
1. Can a YouTube creator credibly sell to Fortune 500 executives?
2. Is $7,500 realistic without enterprise sales infrastructure?
3. Will executives take an online bootcamp seriously vs. a university cert?
4. What if the 800-member Skool community doesn't convert at all?
5. What's the cost of failure if the first cohort flops publicly?
6. Is the self-paced $2,000 course actually the trap (builds wrong audience)?
7. What risks is everyone else NOT talking about?

Don't be negative for its own sake — find the REAL risks that could kill this.""",
        output_path=f"{BASE}/devils_advocate.md",
    )

    board = [market_researcher, audience_analyst, financial_modeler, competitive_strategist, devils_advocate]
    runner.run_parallel(board, shared_context="")

    # Phase 2: Each member shares top finding, Devil's Advocate challenges 2 others
    print("\nPhase 2: Board debate — Devil's Advocate challenges assumptions...")

    top_findings = "\n\n".join(
        f"### {a.name}:\n{(a.result or '')[:500]}..." for a in board
    )

    debate_agent = Agent(
        name="Devil's Advocate",
        role="critical risk analyst",
        task="""You've now seen all board members' initial analyses.
Pick the 2 analyses with the weakest assumptions and challenge them directly.
Write a 200-300 word rebuttal for each, citing specific gaps or optimistic assumptions.
Then add any new risks that emerged from reading the other analyses.""",
        output_path=f"{BASE}/devils_rebuttal.md",
    )
    runner.run(debate_agent, context=f"All board analyses:\n{top_findings}")

    # Phase 3: Executive brief synthesis
    print("\nPhase 3: Synthesizing executive brief with GO/NO-GO recommendation...")

    all_context = "\n\n---\n\n".join(
        f"## {a.name}\n{a.result}" for a in board if a.result
    ) + f"\n\n## Devil's Advocate Rebuttal\n{debate_agent.result}"

    runner.synthesize(
        task=f"""Synthesize all board analyses into an executive decision brief.

THE DECISION: {decision}

Your output must include:

## RECOMMENDATION
**[GO / NO-GO / CONDITIONAL]**
State the recommendation clearly in the first sentence.

## TOP 3 REASONS FOR THIS RECOMMENDATION

## TOP 3 RISKS REGARDLESS OF DECISION

## IF GO: Suggested launch sequence (step-by-step for first 90 days)
## IF CONDITIONAL: What conditions must be met first?
## IF NO-GO: What to do instead and when to revisit

## DISSENTING VIEW (summarize the strongest counterargument to your recommendation)

Be decisive. The board has debated — now give a clear answer.""",
        context=all_context,
        output_path=f"{BASE}/executive_brief.md",
        role="Board Chair / Decision Synthesizer",
    )

    print(f"\n✓ All outputs saved to {BASE}/")
