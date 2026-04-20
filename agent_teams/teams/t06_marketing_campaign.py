"""
#06 Full Marketing Campaign Launch
4 agents build email, social, ads, and landing page — then cross-channel consistency review.
"""
from agent_teams.core import Agent, AgentRunner

BASE = "outputs/agent_teams_demo/marketing_campaign"

PRODUCT_BRIEF = """
Product: FocusPods Pro — premium noise-canceling headphones, $249
Target: Remote workers and creators who need deep focus in noisy environments

Key selling points:
- 40-hour battery life
- Spatial audio for virtual meetings
- "Focus Mode" — filters human voices but lets through doorbells and alarms
- Built-in Pomodoro timer with haptic taps
- 30-day money-back guarantee on DTC website
"""


def run(product_brief: str = PRODUCT_BRIEF):
    print("\n=== #06 Full Marketing Campaign Launch ===")
    runner = AgentRunner()

    agents = [
        Agent(
            name="Email Marketer",
            role="email marketing specialist and conversion copywriter",
            task=f"""Write a 3-email launch sequence for this product:
{product_brief}

EMAIL 1 — Teaser (2 days before launch):
- Build anticipation, hint at what's coming
- Subject line that gets opens
- Preview text
- Body (150-250 words)
- CTA button text

EMAIL 2 — Launch Day:
- Announce FocusPods Pro
- Lead with 3 key benefits
- Clear buy-now CTA
- Subject line, preview text, body, CTA button

EMAIL 3 — Follow-up (2 days after):
- Social proof angle
- Early buyer reactions (placeholder)
- Second chance CTA
- Urgency: "first 100 buyers get a free carrying case"
- Subject line, preview text, body, CTA button

Format clearly with labels for each section.""",
            output_path=f"{BASE}/email_sequence.md",
        ),
        Agent(
            name="Social Media Manager",
            role="social media content strategist",
            task=f"""Create platform-specific launch content for this product:
{product_brief}

1. LINKEDIN POST (150-250 words)
   - Professional angle: productivity and remote work
   - Thought leadership tone
   - End with a question

2. TWITTER/X THREAD (7 tweets)
   - Hook tweet first, CTA last
   - Each tweet self-contained
   - Number them 1/7, 2/7, etc.

3. INSTAGRAM CAPTION
   - Lifestyle angle, short and punchy
   - Hashtag strategy (15-20 relevant tags)
   - Story sticker CTA suggestion

4. TIKTOK SCRIPT (30 seconds)
   - Hook: "POV: your coworker won't stop talking during your deep work block"
   - Show the problem, introduce the solution
   - Include visual direction notes in [brackets]""",
            output_path=f"{BASE}/social_content.md",
        ),
        Agent(
            name="Ad Copywriter",
            role="performance marketing and paid ad copywriter",
            task=f"""Write 3 ad copy variations for this product:
{product_brief}

VARIATION A — Problem-Agitation-Solution:
Noisy environment → can't focus → FocusPods fix it
- Headline (max 40 chars)
- Body (max 125 chars)
- CTA text
- Targeting suggestions (audience, interests, platforms)

VARIATION B — Social Proof / Results:
"87% of beta testers reported deeper focus in week 1"
- Headline (max 40 chars)
- Body (max 125 chars)
- CTA text
- Targeting suggestions

VARIATION C — Us-vs-Them Comparison:
AirPods Max vs FocusPods Pro feature table framing
- Headline (max 40 chars)
- Body (max 125 chars)
- CTA text
- Feature comparison table (5 key features)
- Targeting suggestions

For each variation also suggest: best platform (Meta/Google/YouTube/TikTok) and why.""",
            output_path=f"{BASE}/ad_copy.md",
        ),
        Agent(
            name="Landing Page Writer",
            role="conversion rate optimization and landing page copywriter",
            task=f"""Write full copy for a product landing page:
{product_brief}

HERO SECTION
- Headline (bold, benefit-driven)
- Subheadline (1-2 sentences)
- CTA button text
- Social proof bar: "As seen in TechCrunch, Wired, The Verge" [placeholder]

FEATURE BLOCKS (one for each key feature)
For Focus Mode, 40hr Battery, Spatial Audio, Pomodoro Timer:
- [Icon placeholder]
- Feature headline (3-5 words)
- 2-sentence description

SOCIAL PROOF SECTION
- 3 placeholder testimonials: one from a remote worker, one creator, one startup CEO
- Include name, title, and 2-3 sentence quote each

COMPARISON TABLE
FocusPods Pro vs AirPods Max vs Sony WH-1000XM6
(Rows: Price, Battery, Noise Cancellation, Focus Mode, Pomodoro Timer, Warranty)

FAQ SECTION (5 questions)
Address: price, comfort over long sessions, device compatibility, return policy, delivery time

FINAL CTA SECTION
- Urgency element
- Guarantee reminder
- Big CTA button""",
            output_path=f"{BASE}/landing_page_copy.md",
        ),
    ]

    print("\nPhase 1: All 4 content agents working in parallel...")
    runner.run_parallel(agents)

    all_content = "\n\n---\n\n".join(
        f"## {a.name}\n{a.result}" for a in agents if a.result
    )

    print("\nPhase 2: Cross-channel consistency review...")
    runner.synthesize(
        task=f"""Review all campaign content for cross-channel consistency.

PRODUCT BRIEF:
{product_brief}

Check:
1. MESSAGING CONSISTENCY — Does the same core value proposition appear in every channel?
2. TONE ALIGNMENT — Is the voice consistent across email, social, ads, and landing page?
3. CONTRADICTIONS — Are there any conflicting claims or specs between channels?
4. CTA ALIGNMENT — Do all CTAs point to the same destination / use consistent language?
5. GAPS — Any key selling point missing from any channel?

Then write:
## CAMPAIGN MESSAGING GUIDELINES
- The one-sentence brand promise for FocusPods Pro
- 3 approved messaging pillars (use these consistently)
- Tone of voice guide (3-4 descriptors with examples)
- What to avoid saying (off-brand language or claims)

## ISSUES FOUND (if any)
Flag and suggest fixes""",
        context=all_content,
        output_path=f"{BASE}/campaign_summary.md",
        role="Brand Strategy Director",
    )

    print(f"\n✓ All outputs saved to {BASE}/")
