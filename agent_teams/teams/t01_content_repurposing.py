"""
#01 Content Repurposing Pipeline
Repurpose a single video transcript into 4 platform-specific pieces with zero overlap.
"""
from pathlib import Path
from agent_teams.core import Agent, AgentRunner

BASE = "outputs/agent_teams_demo/content_repurposing"


def run(transcript_path: str = "transcript.md"):
    print("\n=== #01 Content Repurposing Pipeline ===")
    runner = AgentRunner()

    transcript = Path(transcript_path).read_text(encoding="utf-8")

    agents = [
        Agent(
            name="Blog Writer",
            role="expert blog content writer",
            task=f"""Read this transcript and identify the 3 most compelling insights.
Then transform it into a 1,200-word blog post.
Structure: hook paragraph, 3-5 subheadings with key insights, conclusion with CTA.
Write in first person.

TRANSCRIPT:
{transcript}

Save your chosen 3 insights at the top of your output (so other agents can see them),
then write the full blog post below.""",
            output_path=f"{BASE}/blog_post.md",
        ),
        Agent(
            name="LinkedIn Writer",
            role="expert LinkedIn content strategist",
            task=f"""Read this transcript and identify the 3 most compelling insights.
Then write a LinkedIn post (150-250 words).
Use a hook line, 3 key takeaways as short paragraphs, and end with a question to drive comments.
No hashtag spam — max 3 relevant hashtags.

TRANSCRIPT:
{transcript}

Save your chosen 3 insights at the top of your output (so other agents can see them),
then write the full LinkedIn post below.""",
            output_path=f"{BASE}/linkedin_post.md",
        ),
        Agent(
            name="Newsletter Writer",
            role="expert email newsletter writer",
            task=f"""Read this transcript and identify the 3 most compelling insights.
Then write an email newsletter edition (300-500 words).
Include: Subject line + preview text + body. Conversational tone, one clear CTA.

TRANSCRIPT:
{transcript}

Save your chosen 3 insights at the top of your output (so other agents can see them),
then write the full newsletter below.""",
            output_path=f"{BASE}/newsletter.md",
        ),
        Agent(
            name="Twitter Thread Writer",
            role="expert Twitter/X content creator",
            task=f"""Read this transcript and identify the 3 most compelling insights.
Then write a 7-10 tweet thread.
Tweet 1 is the hook. Each tweet is self-contained but builds on the last.
Final tweet is a CTA.

TRANSCRIPT:
{transcript}

Save your chosen 3 insights at the top of your output (so other agents can see them),
then write the full thread below.""",
            output_path=f"{BASE}/twitter_thread.md",
        ),
    ]

    print("\nPhase 1: All 4 agents writing in parallel...")
    runner.run_parallel(agents)

    # Build shared context from all agents' chosen insights
    insights_context = "\n\n".join(
        f"=== {a.name} chose these insights ===\n{a.result[:600]}" for a in agents if a.result
    )

    print("\nPhase 2: Synthesis — comparing angles and flagging overlaps...")
    runner.synthesize(
        task="""Review all 4 pieces of content below. Write a synthesis summary that:
1. Lists the angle/insight each platform led with
2. Confirms each piece feels fresh and non-repetitive
3. Flags any messaging inconsistencies or overlapping angles
4. Gives a brief recommendation if any piece needs adjustment""",
        context=insights_context,
        output_path=f"{BASE}/synthesis_summary.md",
        role="Content Strategy Reviewer",
    )

    print(f"\n✓ All outputs saved to {BASE}/")
