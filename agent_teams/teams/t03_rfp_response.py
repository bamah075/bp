"""
#03 RFP Response Generator
Parallel analysis → parallel section writing → full proposal with consistency check.
"""
from agent_teams.core import Agent, AgentRunner

BASE = "outputs/agent_teams_demo/rfp_response"

RFP_URL = "https://canadabuys.canada.ca/en/tender-opportunities/tender-notice/bc006-2026"

COMPANY_PROFILE = """
We are a 15-person AI consulting firm specializing in building custom automation workflows
for mid-market companies. We use tools like Claude Code, n8n, and Supabase.
Our average project size is $25K-$75K and we've completed 40+ projects in the last 18 months.
Our differentiator: we build systems clients can maintain themselves after handoff.
"""


def run(rfp_url: str = RFP_URL, company_profile: str = COMPANY_PROFILE):
    print("\n=== #03 RFP Response Generator ===")
    runner = AgentRunner()

    # Phase 1: RFP Analyst + Capability Researcher in parallel
    print("\nPhase 1: RFP analysis and capability mapping (parallel)...")

    rfp_analyst = Agent(
        name="RFP Analyst",
        role="government procurement specialist",
        task=f"""Analyze the RFP at this URL: {rfp_url}

If you cannot access the URL directly, note that and create a realistic template based
on a typical government IT/consulting RFP.

Extract and document:
1. All explicit requirements (numbered list)
2. Evaluation criteria and their weights/importance
3. Submission requirements (format, deadline, page limits)
4. Key questions or ambiguities needing clarification
5. Contract value and duration if stated""",
        output_path=f"{BASE}/rfp_analysis.md",
    )

    capability_researcher = Agent(
        name="Capability Researcher",
        role="proposal strategy specialist",
        task=f"""Build a capability matrix for our company based on this profile:

{company_profile}

Map our strengths to common RFP categories:
- Technical approach
- Team qualifications
- Past performance
- Management approach
- Pricing strategy

For each category:
- Rate our strength (Strong / Moderate / Developing)
- List 2-3 specific evidence points
- Identify our top differentiator in this area

Then identify our 3-5 overall differentiators that should appear throughout the proposal.""",
        output_path=f"{BASE}/capability_matrix.md",
    )

    runner.run_parallel([rfp_analyst, capability_researcher])

    shared_context = f"""RFP ANALYSIS:
{rfp_analyst.result}

CAPABILITY MATRIX:
{capability_researcher.result}"""

    # Phase 2: Two section writers in parallel
    print("\nPhase 2: Writing proposal sections (parallel)...")

    writer_a = Agent(
        name="Section Writer A",
        role="senior proposal writer",
        task="""Using the RFP analysis and capability matrix, write these sections:

1. EXECUTIVE SUMMARY (1 page / ~400 words)
   - Open with the client's core need
   - State our solution and key differentiator
   - Preview the value we'll deliver

2. TECHNICAL APPROACH
   - Our methodology for this engagement
   - Tools and technologies we'll use
   - How we address the specific RFP technical requirements

3. MANAGEMENT APPROACH
   - Project governance and oversight
   - Communication and reporting cadence
   - Risk management approach

Use professional proposal language. Reference the RFP requirements directly.""",
        output_path=f"{BASE}/proposal_sections_a.md",
    )

    writer_b = Agent(
        name="Section Writer B",
        role="senior proposal writer",
        task="""Using the RFP analysis and capability matrix, write these sections:

1. TEAM QUALIFICATIONS
   - Team structure and roles
   - [Placeholder: 3 key team member bios with relevant experience]
   - Relevant certifications and expertise

2. PAST PERFORMANCE
   - [Placeholder: 3 case studies showing similar work]
   - Each case study: client (anonymized), challenge, our solution, measurable result

3. PRICING NARRATIVE (strategic framing only, no actual numbers)
   - Our value-based pricing philosophy
   - How we structure engagements to reduce client risk
   - Why our price-to-value ratio is competitive

Use professional proposal language. Reference the RFP requirements directly.""",
        output_path=f"{BASE}/proposal_sections_b.md",
    )

    runner.run_parallel([writer_a, writer_b], shared_context=shared_context)

    # Phase 3: Synthesis and cross-reference check
    print("\nPhase 3: Cross-reference check and final assembly...")
    full_context = f"""{shared_context}

SECTION A (Executive Summary, Technical, Management):
{writer_a.result}

SECTION B (Team, Past Performance, Pricing):
{writer_b.result}"""

    runner.synthesize(
        task="""Assemble and review the full proposal. Your output should be:

PART 1 — CONSISTENCY REVIEW
Check for:
- Consistent tone and terminology across all sections
- No contradictions between sections
- Every RFP requirement addressed (cross-reference against analyst's checklist)
- Any requirements not addressed (flag with [GAP])

PART 2 — FULL ASSEMBLED PROPOSAL
Combine all sections in proper order with a professional cover page:
1. Cover Page
2. Executive Summary
3. Technical Approach
4. Management Approach
5. Team Qualifications
6. Past Performance
7. Pricing Narrative
8. Appendix (placeholder)""",
        context=full_context,
        output_path=f"{BASE}/full_proposal.md",
        role="Senior Proposal Manager",
    )

    print(f"\n✓ All outputs saved to {BASE}/")
