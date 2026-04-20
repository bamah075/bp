# #02 Pitch Deck Builder (with Task Dependencies)

**Use case:** Research-backed pitch deck with sequential handoffs — Researcher → Writer → Designer.

---

Create an agent team to build a 12-slide pitch deck about how AI automation is transforming small business operations in 2026.

Spawn 3 teammates with task dependencies:

1. **Researcher** — Find 8-10 key data points, stats, and supporting evidence about AI automation adoption among small businesses. For each data point, include the source and a one-sentence explanation of why it matters. Save findings to outputs/agent_teams_demo/pitch_deck/research_brief.md. **This task must complete before the Writer begins.**

2. **Slide Writer** — Using the Researcher's brief, write the content for a 12-slide deck:
   - Slide 1: Title + subtitle
   - Slide 2: The problem / opportunity
   - Slides 3-4: Key data points (pick the 4 strongest from research)
   - Slides 5-8: Core argument / solution (one point per slide)
   - Slide 9: Case study or example
   - Slide 10: Objection handling
   - Slide 11: Summary / key takeaway
   - Slide 12: CTA / next steps

   Each slide: headline (max 8 words), 3-4 bullet points (max 12 words each), and speaker notes (2-3 sentences). Save to outputs/agent_teams_demo/pitch_deck/slide_content.md. **This task must complete before the Designer begins.**

3. **Designer** — Using the Slide Writer's content, build the actual .pptx file using Python (python-pptx library). Use a clean, professional design: dark background (#1a1a2e), white text, accent color (#E07A4F). Include proper slide layouts, consistent fonts (Arial or Helvetica), and logical visual hierarchy. Save to outputs/agent_teams_demo/pitch_deck/pitch_deck.pptx.

Require plan approval for the Designer before they start building — I want to review the design approach first.
