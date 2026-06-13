# 🎤 Maya Quick Commands Reference

## Voice Commands Cheat Sheet

### Meeting Management
| Command | What It Does |
|---------|-------------|
| `start meeting` | Begin capturing meeting notes |
| `add note [text]` | Add a note to current meeting |
| `action item [task] for [person]` | Log action item with owner |
| `end meeting` | End meeting and get summary |

### Calendar & Schedule
| Command | What It Does |
|---------|-------------|
| `what's my schedule today?` | View today's appointments |
| `show my schedule` | View today's appointments |
| `week summary` | See your entire week |
| `what's this week?` | See your entire week |

### Tasks & To-Do's
| Command | What It Does |
|---------|-------------|
| `add task [description]` | Create a new to-do item |
| `add task [task] for [date]` | Create task with due date |
| `my tasks` | List all pending tasks |
| `to-do list` | List all pending tasks |

### Reminders
| Command | What It Does |
|---------|-------------|
| `set reminder [message] on [date] at [time]` | Create a reminder |
| `remind me on [date] at [time]` | Create a reminder |

### Automation
| Command | What It Does |
|---------|-------------|
| `automate [task description]` | Get automation suggestions |
| `help with automation [task]` | Get platform-specific guidance |
| `zapier setup [from] to [to]` | Zapier integration guide |
| `goHighLevel automation [type]` | GHL setup instructions |
| `copilot help with [code task]` | Code automation suggestions |

### Tasks & Help
| Command | What It Does |
|---------|-------------|
| `help me with [task]` | Get structured assistance |
| `draft email to [person] about [subject]` | Email template |
| `help me plan [goal]` | Create action plan |
| `analyze [data description]` | Data analysis framework |
| `solve this problem [problem]` | Problem-solving guide |
| `brainstorm ideas for [topic]` | Brainstorming session |

### Research
| Command | What It Does |
|---------|-------------|
| `search reddit for [topic]` | Research topic on Reddit |
| `small business automation australia` | Market research |
| `what are pain points for [industry]` | Research pain points |

### General
| Command | What It Does |
|---------|-------------|
| `hello` | Greeting |
| `what can you do` | List capabilities |
| `tell me a joke` | Get a joke |
| `tell me a fact` | Learn something new |
| `help` | Get general help |

---

## 🎯 Common Workflows

### Daily Standup (Morning)
```
1. "Good morning Maya"
2. "What's my schedule today?"
3. "My tasks"
4. "Any reminders for today?"
```

### Meeting Workflow
```
1. "Start meeting"
2. "Add note [topic 1]"
3. "Add note [topic 2]"
4. "Action item [task] for [person]"
5. "End meeting"
```

### Task Management
```
1. "Add task [high priority task]"
2. "Add task [medium priority task]"
3. "My tasks"
4. "Add appointment meeting on [date] at [time]"
```

### Automation Setup
```
1. "I want to automate [task]"
2. "Zapier setup [app1] to [app2]"
3. "How do I deploy this?"
```

### Get Help
```
1. "Help me with [task]"
2. "Draft email to [person] about [subject]"
3. "Brainstorm ideas for [topic]"
```

---

## 🎤 How to Use Voice Commands

### In GUI
1. Click the **🎤 Listen** button
2. Speak clearly (Maya listens for 3 seconds)
3. Wait for response
4. Click **Listen** again for next command

### In Terminal
```bash
python3 -c "
from Brain.smart_brain import _smart_brain
print(_smart_brain.process_command('your command here'))
"
```

---

## 💡 Pro Tips

### For Meetings
- Use "add note" for key discussion points
- Use "action item" for clear ownership
- Maya auto-generates summaries automatically

### For Tasks
- Add high priority items first
- Use due dates for important tasks
- Check "My tasks" regularly

### For Automation
- Describe what you want to automate clearly
- Maya will suggest platforms
- Follow the step-by-step guide

### For Help
- Be specific about what you need help with
- Use keywords like "plan", "analyze", "draft"
- Maya provides structured frameworks

---

## 🔧 Format Guide

### Date Format
`YYYY-MM-DD` (Example: 2026-06-13)

### Time Format
`HH:MM` (24-hour, Example: 14:30)

### Task Priority
- `high` - Urgent, must do today
- `medium` - Important, this week
- `low` - Can be delayed

---

## ❓ Troubleshooting

### Command Not Working?
1. Try a simpler version (e.g., "my tasks" instead of "show all my tasks")
2. Check the format (dates, times)
3. Use keywords from the command table

### Maya Not Understanding?
1. Speak more clearly
2. Use shorter phrases
3. Check if a related feature exists

### Need More Details?
1. Read `JARVIS_ENTERPRISE.md` for full documentation
2. Check specific module files in `Brain/` folder
3. Test commands in terminal first

---

## 📚 Full Documentation

For complete details, see:
- **JARVIS_ENTERPRISE.md** - Full feature guide
- **Brain/smart_brain.py** - Main brain logic
- **Brain/meeting_notes.py** - Meeting features
- **Brain/calendar_manager.py** - Calendar features
- **Brain/automation_helper.py** - Automation features
- **Brain/smart_employee.py** - AI assistant features

---

**Need help? Just ask Maya - it's designed to assist with anything!** 🤖✨
