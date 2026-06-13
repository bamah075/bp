# 🧠 Maya Memory & Learning System

## How Maya Gets Smarter Over Time

Maya now has an **intelligent memory system** that:
- ✅ Remembers every question and response
- ✅ Learns from your preferences
- ✅ Improves responses based on feedback
- ✅ Suggests better answers over time
- ✅ Gets smarter with every interaction

---

## Key Features

### 1. **Persistent Memory**
- Stores up to 100 recent interactions
- Saved locally in `~/.maya_memory.json`
- Automatically loads on startup
- No data sent anywhere

### 2. **Pattern Learning**
- Identifies frequently asked questions
- Recognizes question patterns
- Builds knowledge from interactions
- Improves response selection

### 3. **Smart Response Improvement**
- Tracks which responses work best
- Learns from similar questions
- Suggests better answers
- Improves over time

### 4. **Preference Tracking**
- Remembers how you interact
- Adapts to your communication style
- Personalizes responses
- Gets more natural with time

---

## How to Use Memory Features

### Basic Interaction (Automatic)
Maya automatically remembers every conversation:
```
You: "Tell me about automation"
Maya: [learns this question & response]
```

### Check Memory Statistics
```bash
python3 << 'EOF'
from Brain.maya_memory import get_memory_stats
print(get_memory_stats())
EOF
```

**Output:**
```
{
  'total_interactions': 42,
  'good_responses': 38,
  'bad_responses': 2,
  'learned_patterns': 15,
  'improvement_rate': '90.5%'
}
```

### Get Learning Report
```bash
python3 << 'EOF'
from Brain.maya_memory import get_memory_report
print(get_memory_report())
EOF
```

**Shows:**
- Total interactions tracked
- Quality of responses
- Learning patterns discovered
- Overall improvement rate

### Rate a Response (Improve Learning)
Tell Maya if a response was good or bad:

```bash
python3 << 'EOF'
from Brain.maya_memory import _maya_memory

# After getting a response, rate it:
_maya_memory.rate_response(
    "previous response text",
    "good"  # or "bad" or "neutral"
)
EOF
```

### View Memory File
Memory is stored locally:
```bash
cat ~/.maya_memory.json
```

Shows all remembered interactions and patterns.

---

## What Maya Learns

### Question Patterns
Maya learns:
- Your most frequent questions
- Similar question patterns
- Related topics
- Your interests

### Response Quality
Maya tracks:
- Which responses you liked
- Which ones could be better
- What works well
- What doesn't work

### Your Preferences
Maya discovers:
- Your communication style
- Topics you care about
- How detailed you want answers
- Your workflow patterns

---

## Memory Categories

Maya categorizes learning by:

| Category | Examples | What Maya Learns |
|----------|----------|-----------------|
| **Meeting** | "start meeting", "add note" | How to capture meetings better |
| **Calendar** | "add task", "schedule" | Your schedule patterns |
| **Automation** | "automate email", "zapier" | Automation preferences |
| **Smart Help** | "help plan", "analyze" | How you want help structured |
| **Time** | "what time", "when" | Time format preferences |
| **System** | "what system", "platform" | System information needs |
| **Entertainment** | "joke", "fact" | What you find funny/interesting |

---

## Smart Features Enabled by Memory

### 1. **Similar Question Detection**
```python
# If you ask a similar question, Maya can suggest better answers
similar = get_similar_questions("automate workflows")
# Returns: Questions you've asked before + best responses
```

### 2. **Response Suggestion**
```python
# Maya can suggest a better response based on history
better = suggest_better_response(
    "How to automate?",
    "current_response"
)
```

### 3. **Top Questions**
```python
# See what you ask most frequently
top = _maya_memory.get_top_questions()
# Shows your most asked questions
```

### 4. **Improvement Tracking**
```python
# See how Maya is improving
report = get_memory_report()
# Shows learning progress and improvements
```

---

## Memory File Structure

Located at: `~/.maya_memory.json`

```json
{
  "interactions": [
    {
      "timestamp": "2026-06-13T12:53:00",
      "question": "Help me automate email",
      "response": "Here's automation guidance...",
      "category": "automation",
      "quality": "good"
    }
  ],
  "patterns": {
    "automate": [
      {
        "question": "Help me automate email",
        "response": "...",
        "quality": "good",
        "count": 3
      }
    ]
  },
  "ratings": {
    "response_text": {
      "good": 5,
      "bad": 0,
      "neutral": 2
    }
  },
  "preferences": {}
}
```

---

## Privacy & Data

### Your Privacy is Protected
✅ All data stored **locally** on your machine  
✅ No cloud sync or external storage  
✅ No data sent to servers  
✅ You own all your data  
✅ Easy to delete anytime  

### Delete All Memory
```bash
python3 << 'EOF'
from Brain.maya_memory import _maya_memory
_maya_memory.reset_memory()
print("All memory cleared!")
EOF
```

Or delete the file:
```bash
rm ~/.maya_memory.json
```

---

## How Learning Improves Maya

### Example 1: Better Automation Guidance
```
Interaction 1:
You: "How do I automate email?"
Maya: "[Generic response]"
You: "That wasn't detailed enough"
[Maya marks as low quality]

Interaction 2:
You: "How do I automate email?"
Maya: "[More detailed response based on learning]"
You: "Perfect!"
[Maya marks as high quality]

Future Interactions:
Maya automatically suggests the detailed response!
```

### Example 2: Learning Your Style
```
Interaction 1:
You: "Tell me a joke"
Maya: [Technical programming joke]
You: [Bad rating]

Interaction 2:
You: "Make me laugh"
Maya: [Different type of joke]
You: [Good rating]

Future Interactions:
Maya learns your humor preference and adapts!
```

---

## Memory Statistics

### What Gets Tracked
- Total interactions
- Response quality ratings
- Learned patterns
- Improvement rate
- Most asked questions
- Category breakdown

### View Anytime
```bash
python3 -c "from Brain.maya_memory import get_memory_stats; import json; print(json.dumps(get_memory_stats(), indent=2))"
```

---

## Advanced Features

### Get Similar Questions
```python
from Brain.maya_memory import get_similar_questions

similar = get_similar_questions("automation help")
# Returns similar questions you've asked before
# With the best responses for each
```

### Check Top Questions
```python
from Brain.maya_memory import _maya_memory

top = _maya_memory.get_top_questions(limit=10)
# Shows your 10 most frequent questions
```

### Get Improvement Suggestions
```python
from Brain.maya_memory import _maya_memory

suggestions = _maya_memory.get_improvement_suggestions()
# Shows topics where Maya could do better
```

---

## How to Rate Responses

### After Each Response
You can rate Maya's response:

```bash
# Good response
python3 -c "from Brain.maya_memory import _maya_memory; _maya_memory.rate_response('response_text', 'good')"

# Bad response
python3 -c "from Brain.maya_memory import _maya_memory; _maya_memory.rate_response('response_text', 'bad')"

# Neutral
python3 -c "from Brain.maya_memory import _maya_memory; _maya_memory.rate_response('response_text', 'neutral')"
```

---

## Summary

Maya's memory system makes her **smarter with every interaction**:

1. **Automatic Learning** - Every conversation is remembered
2. **Pattern Recognition** - Learns your question patterns
3. **Quality Tracking** - Knows which responses work best
4. **Smart Suggestions** - Recommends better answers
5. **Personalization** - Adapts to your style
6. **Local Privacy** - Everything stored locally
7. **Continuous Improvement** - Gets better over time

---

## Get Started with Memory

Maya is **automatically learning** right now! Just use her normally, and she'll get smarter with every interaction.

**To check her progress:**
```bash
python3 << 'EOF'
from Brain.maya_memory import get_memory_report
print(get_memory_report())
EOF
```

**The more you use Maya, the smarter she becomes!** 🧠✨
