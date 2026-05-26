#!/usr/bin/env python3
"""
Daily Brief Generator - Generates daily briefs using Claude API
"""

import os
import json
from datetime import datetime
from anthropic import Anthropic

client = Anthropic()

def generate_daily_brief(topics: list[str] = None) -> str:
    """
    Generate a daily brief using Claude with multi-turn conversation.

    Args:
        topics: List of topics to cover (defaults to Substack AI trends and AI agents)
    """
    if not topics:
        topics = [
            "Substack trends in AI and emerging technologies",
            "Building operating systems using AI agents",
            "AI agent frameworks and tooling innovations"
        ]

    conversation_history = []

    # First turn: Request brief outline
    print("📋 Generating daily brief structure...")
    outline_prompt = f"""Create a brief outline for today's ({datetime.now().strftime('%B %d, %Y')}) daily brief covering these topics:
{chr(10).join(f'- {topic}' for topic in topics)}

Format as a numbered list of 3-5 key sections."""

    conversation_history.append({
        "role": "user",
        "content": outline_prompt
    })

    outline_response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=500,
        messages=conversation_history
    )

    outline_text = outline_response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": outline_text
    })

    # Second turn: Expand outline into full brief
    print("✍️ Expanding into full brief...")
    expansion_prompt = """Now expand this outline into a comprehensive daily brief. For each section:
- Add 2-3 key insights
- Include actionable takeaways
- Keep it concise (2-3 sentences per point)

Use markdown formatting."""

    conversation_history.append({
        "role": "user",
        "content": expansion_prompt
    })

    brief_response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1500,
        messages=conversation_history
    )

    brief_text = brief_response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": brief_text
    })

    # Third turn: Add summary and next steps
    print("🎯 Finalizing brief with summary...")
    summary_prompt = """Add a brief summary section at the end with:
- Top 3 key takeaways for the day
- One recommended action for the newsletter
- Sign-off line"""

    conversation_history.append({
        "role": "user",
        "content": summary_prompt
    })

    final_response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=500,
        messages=conversation_history
    )

    final_text = final_response.content[0].text

    # Combine all parts
    full_brief = f"""# Daily Brief - {datetime.now().strftime('%B %d, %Y')}

{outline_text}

---

{brief_text}

---

{final_text}
"""

    return full_brief

def save_brief(brief_content: str, output_file: str = None) -> str:
    """Save the brief to a file."""
    if not output_file:
        date_str = datetime.now().strftime("%Y-%m-%d")
        output_file = f"daily_briefs/{date_str}_brief.md"

    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)

    with open(output_file, "w") as f:
        f.write(brief_content)

    print(f"✅ Brief saved to: {output_file}")
    return output_file

if __name__ == "__main__":
    brief = generate_daily_brief()
    print("\n" + "="*60)
    print(brief)
    print("="*60 + "\n")
    save_brief(brief)
