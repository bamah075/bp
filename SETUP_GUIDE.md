# 🚀 Maya Enterprise Setup Guide

## Complete Installation & Configuration

---

## Phase 1: Installation ✅ (Already Done!)

Maya is ready to use! All core modules are installed:
- ✅ Smart Brain
- ✅ Meeting Notes
- ✅ Calendar Manager
- ✅ Automation Helper
- ✅ Smart Employee AI
- ✅ Reddit Scraper

No additional installation needed!

---

## Phase 2: Quick Start

### Launch Maya
```bash
cd ~/bp
bash JARVIS_FUTURISTIC.command
```

### Test in Terminal
```bash
python3 -c "
from Brain.smart_brain import _smart_brain
print(_smart_brain.process_command('start meeting'))
"
```

---

## Phase 3: Configure Cloud Integration (Optional)

### Option A: Google Workspace Integration

#### Prerequisites:
- Google account
- Google Drive with sufficient space
- Google Calendar access

#### Setup Steps:

1. **Create Google Service Account**
   ```bash
   # Go to Google Cloud Console
   # https://console.cloud.google.com/
   # Create new project "Maya"
   # Enable Google Drive API
   # Enable Google Calendar API
   # Create service account
   # Download JSON key file
   ```

2. **Install Google Libraries**
   ```bash
   pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

3. **Create Google Integration Module**
   ```bash
   # File: Brain/google_drive_manager.py
   # This module will sync Maya data with Google Drive
   ```

4. **Configure Environment**
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export GOOGLE_SERVICE_ACCOUNT_KEY="/path/to/service-account-key.json"
   export JARVIS_GOOGLE_DRIVE_FOLDER_ID="your-folder-id"
   export JARVIS_GOOGLE_CALENDAR_ID="your-calendar-id"
   ```

#### Features Once Configured:
- Meeting notes auto-saved to Google Drive
- Appointments synced with Google Calendar
- Tasks synced with Google Tasks
- Email drafts saved to Google Drive
- Access Maya data from anywhere

### Option B: Automation API Keys

#### Zapier Integration
```bash
# Set environment variable
export ZAPIER_WEBHOOK="https://hooks.zapier.com/hooks/catch/..."
```

#### GoHighLevel Integration
```bash
# Set environment variable
export GHL_API_KEY="your-ghl-api-key"
```

#### GitHub Copilot Integration
```bash
# Set environment variable
export COPILOT_API_KEY="your-copilot-api-key"
```

#### Claude API Integration
```bash
# Set environment variable
export CLAUDE_API_KEY="your-claude-api-key"
```

---

## Phase 4: Configuration Files

### Create Config File
```bash
# File: ~/.jarvis_config.json
{
  "user": {
    "name": "Your Name",
    "email": "your.email@example.com",
    "timezone": "UTC"
  },
  "integrations": {
    "google_workspace": {
      "enabled": false,
      "service_account_key": "/path/to/key.json"
    },
    "zapier": {
      "enabled": false,
      "webhook_url": ""
    },
    "goHighLevel": {
      "enabled": false,
      "api_key": ""
    },
    "github_copilot": {
      "enabled": false,
      "api_key": ""
    },
    "claude": {
      "enabled": false,
      "api_key": ""
    }
  },
  "preferences": {
    "default_meeting_duration": "60 minutes",
    "default_task_priority": "medium",
    "language": "en",
    "theme": "dark"
  }
}
```

---

## Phase 5: Verify Installation

### Check All Modules Load
```bash
python3 << 'EOF'
import sys
print("Checking Maya modules...")

modules = [
    'Brain.smart_brain',
    'Brain.meeting_notes',
    'Brain.calendar_manager',
    'Brain.automation_helper',
    'Brain.smart_employee',
    'Brain.reddit_scraper'
]

for module in modules:
    try:
        __import__(module)
        print(f"✓ {module}")
    except Exception as e:
        print(f"✗ {module}: {e}")

print("\nAll modules ready! ✅")
EOF
```

### Run Tests
```bash
python3 << 'EOF'
from Brain.smart_brain import _smart_brain

tests = {
    'greeting': 'hello',
    'meeting': 'start meeting',
    'task': 'add task test',
    'schedule': 'what is my schedule',
    'automation': 'automate email',
    'help': 'help me plan my day'
}

print("Running Maya tests...\n")
for feature, command in tests.items():
    try:
        result = _smart_brain.process_command(command)
        status = "✓" if result else "✗"
        print(f"{status} {feature}: {command}")
    except Exception as e:
        print(f"✗ {feature}: {e}")

print("\nTests complete! 🎉")
EOF
```

---

## Phase 6: Daily Usage Setup

### Create Alias (Optional)
```bash
# Add to ~/.bashrc or ~/.zshrc
alias jarvis='cd ~/bp && bash JARVIS_FUTURISTIC.command'
```

### Create Scheduler Job (Optional)
```bash
# macOS - Create launchd job
# ~/.config/launchd/com.jarvis.remind.plist
# Run reminders check every hour
```

### Enable Notifications (Optional)
```bash
# Configure system notifications for reminders
# Enable calendar sync notifications
# Enable meeting notifications
```

---

## Phase 7: Advanced Configuration

### Custom Response Sets
Add your own response variants in `Brain/smart_brain.py`:
```python
self.response_pool["custom_greeting"] = [
    "Your custom response 1",
    "Your custom response 2",
]
```

### Add Custom Commands
Extend `process_command()` in `Brain/smart_brain.py`:
```python
elif "your_keyword" in text_lower:
    response = "Your custom logic here"
```

### Integration Hooks
Create custom integrations:
```python
# File: Brain/custom_integration.py
class CustomIntegration:
    def __init__(self):
        self.api_key = os.getenv('CUSTOM_API_KEY')
    
    def custom_action(self, data):
        # Your integration logic
        pass
```

---

## 🔧 Troubleshooting

### Module Import Errors
```bash
# Ensure all dependencies installed
pip install -r requirements-mac.txt

# Verify Python version (3.9+)
python3 --version
```

### Google Integration Not Working
```bash
# Check environment variables set
echo $GOOGLE_SERVICE_ACCOUNT_KEY

# Verify service account has correct permissions
# In Google Cloud Console: IAM > Service Accounts
```

### Automation APIs Not Working
```bash
# Check API keys configured
echo $ZAPIER_WEBHOOK
echo $GHL_API_KEY
echo $COPILOT_API_KEY
echo $CLAUDE_API_KEY

# Verify API keys are valid and active
```

### Maya Not Responding
```bash
# Check if Python process is running
ps aux | grep jarvis_gui_futuristic

# Kill and restart if needed
pkill -f jarvis_gui_futuristic
python3 jarvis_gui_futuristic.py
```

---

## 📊 Feature Checklist

### Core Features ✅
- [x] Voice input/output
- [x] Meeting notes capture
- [x] Calendar management
- [x] Task management
- [x] Automation guidance
- [x] Smart employee AI
- [x] Market research (Reddit)

### Optional Features (Need Setup)
- [ ] Google Drive sync
- [ ] Google Calendar sync
- [ ] Zapier automation
- [ ] GoHighLevel integration
- [ ] GitHub Copilot integration
- [ ] Claude API integration
- [ ] Email notifications
- [ ] System reminders

### Planned Features
- [ ] Slack integration
- [ ] Email integration
- [ ] Mobile app
- [ ] Team collaboration
- [ ] Advanced analytics
- [ ] Machine learning models

---

## 🚀 Performance Optimization

### Reduce Memory Usage
```bash
# Disable Reddit scraper in config
# Disable cloud sync
# Clear old meeting notes regularly
```

### Improve Response Time
```bash
# Use local storage instead of cloud
# Disable logging during peak hours
# Optimize command matching patterns
```

---

## 🔐 Security Checklist

- [ ] Secure API keys in environment variables
- [ ] Use strong Google account password
- [ ] Enable 2FA on Google account
- [ ] Restrict service account permissions
- [ ] Regularly rotate API keys
- [ ] Monitor API usage
- [ ] Backup important data
- [ ] Encrypt local storage if needed

---

## 📞 Support Resources

### Documentation
- `JARVIS_ENTERPRISE.md` - Full feature guide
- `QUICK_COMMANDS.md` - Command reference
- `INTELLIGENT_JARVIS.md` - SmartBrain details
- `FUTURISTIC_GUIDE.md` - GUI features
- `REDDIT_SCRAPER.md` - Research capabilities

### Code Files
- `Brain/smart_brain.py` - Main logic
- `Brain/meeting_notes.py` - Meeting features
- `Brain/calendar_manager.py` - Calendar features
- `Brain/automation_helper.py` - Automation features
- `Brain/smart_employee.py` - AI assistant

### Troubleshooting
1. Check documentation files
2. Review module docstrings
3. Test in terminal
4. Check environment variables
5. Review logs for errors

---

## ✅ Next Steps

1. **Start using Maya** - Launch the GUI and try commands
2. **Test all features** - Try each module to understand capabilities
3. **Configure integrations** - Setup cloud/API integrations as needed
4. **Create workflows** - Build custom commands and automations
5. **Optimize usage** - Fine-tune settings for your workflow

---

**Maya is ready to work for you!** 🤖✨

Start with voice commands, explore features, configure integrations as needed.
