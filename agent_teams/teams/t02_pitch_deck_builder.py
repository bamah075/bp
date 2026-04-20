"""
#02 Pitch Deck Builder (with Task Dependencies)
Sequential: Researcher → Slide Writer → Designer (.pptx)
"""
import subprocess
import sys
from agent_teams.core import Agent, AgentRunner

BASE = "outputs/agent_teams_demo/pitch_deck"
TOPIC = "how AI automation is transforming small business operations in 2026"


def run(require_approval: bool = True):
    print("\n=== #02 Pitch Deck Builder ===")
    runner = AgentRunner()

    # Stage 1: Researcher
    print("\nStage 1: Researcher gathering data points...")
    researcher = Agent(
        name="Researcher",
        role="business research analyst",
        task=f"""Find 8-10 key data points, stats, and supporting evidence about {TOPIC}.
For each data point include:
- The stat or finding
- Source (publication, study, or credible org)
- One sentence explaining why it matters for a pitch deck

Format as a numbered list. Be specific with numbers and percentages.""",
        output_path=f"{BASE}/research_brief.md",
    )
    runner.run(researcher)

    # Stage 2: Slide Writer (depends on Researcher)
    print("\nStage 2: Slide Writer building content...")
    writer = Agent(
        name="Slide Writer",
        role="presentation content specialist",
        task=f"""Using the research brief provided, write content for a 12-slide deck on: {TOPIC}

For EACH slide provide:
- Slide number and title
- Headline (max 8 words)
- 3-4 bullet points (max 12 words each)
- Speaker notes (2-3 sentences)

Slides:
1. Title + subtitle
2. The problem / opportunity
3-4. Key data points (pick the 4 strongest from research)
5-8. Core argument / solution (one point per slide)
9. Case study or example
10. Objection handling
11. Summary / key takeaway
12. CTA / next steps""",
        output_path=f"{BASE}/slide_content.md",
    )
    runner.run(writer, context=f"Research Brief:\n{researcher.result}")

    # Plan approval gate
    if require_approval:
        print(f"\n--- PLAN APPROVAL REQUIRED ---")
        print(f"Slide content saved to: {BASE}/slide_content.md")
        print("Review the slide content, then press Enter to continue to Designer...")
        input("  > ")

    # Stage 3: Designer (depends on Slide Writer)
    print("\nStage 3: Designer building .pptx file...")

    designer = Agent(
        name="Designer",
        role="Python presentation developer using python-pptx",
        task=f"""Using the slide content provided, write a complete Python script that builds a .pptx file.

Requirements:
- Use python-pptx library
- Dark background: #1a1a2e
- White text for body
- Accent color: #E07A4F for headings/highlights
- Consistent fonts: Arial or Calibri
- Each slide uses the exact content from the brief
- Save the output file to: {BASE}/pitch_deck.pptx

Write ONLY the Python script. The script should be complete and runnable.
Start with: from pptx import Presentation""",
        output_path=f"{BASE}/build_deck.py",
    )
    runner.run(designer, context=f"Slide Content:\n{writer.result}")

    # Execute the generated script
    print("\nRunning designer's script to generate .pptx...")
    try:
        result = subprocess.run(
            [sys.executable, f"{BASE}/build_deck.py"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            print(f"  ✓ pitch_deck.pptx created")
        else:
            print(f"  ✗ Script error:\n{result.stderr}")
    except Exception as e:
        print(f"  ✗ Could not execute script: {e}")

    print(f"\n✓ All outputs saved to {BASE}/")
