# 🌟 Maya Web UI - Animated Interface Guide

## Overview

Maya now has a beautiful, modern web-based interface with an **animated Unicorn Studio background**. The web UI provides a sleek, responsive interface while maintaining full connection to Maya's Python backend.

---

## ✨ Features

### Visual Design
- **Unicorn Studio Animated Background** - Stunning real-time animations
- **Dark Mode Theme** - Easy on the eyes with cyan/green color scheme
- **Glassmorphism UI** - Modern frosted glass card design
- **Responsive Layout** - Works on desktop and tablets
- **Smooth Animations** - Fade-ins, transitions, and hover effects

### Functionality
- **Text & Voice Input** - Type commands or use voice recognition
- **Real-time Responses** - Connected to Maya's Python backend
- **System Status** - Monitor APIs, memory, and network status
- **Chat History** - Maintains conversation log
- **Smart Commands** - All of Maya's capabilities available
- **Quick Actions** - Listen, Clear, and Help buttons

---

## 🚀 Quick Start

### Option 1: Launch Web Server (Recommended)

```bash
bash /home/user/bp/launch_maya_web.sh
```

This will:
1. Start the Flask web server
2. Auto-open http://localhost:5000 in your browser
3. Connect to Maya's backend automatically

### Option 2: Manual Launch

```bash
cd /home/user/bp
python3 -m pip install flask flask-cors --quiet
python3 maya_web_server.py
```

Then open: **http://localhost:5000**

---

## 📱 Using the Web Interface

### Text Commands

1. **Type in the input field** at the top
2. **Press Enter** or click **Send**
3. **Maya responds** in the response area

### Voice Commands

1. Click **🎤 Listen** button
2. **Speak your command** clearly
3. Click **Send** to process

### Available Commands

#### Greetings & Info
```
Hi Maya
What can you do?
What's the time?
What's my system info?
```

#### Calendar & Tasks
```
What's my schedule?
What's this week?
Add task: Buy groceries
My tasks
```

#### Weather
```
What's the weather in Sydney?
Forecast in London
Temperature in Tokyo
```

#### AI & Analysis
```
Explain machine learning
Analyze AI trends
Think about automation
What are the benefits of AI?
```

#### Meetings
```
Start meeting
Add note: Discussed project
End meeting
Meeting summary
```

#### Automation
```
Help me automate email
Zapier setup for leads
Workflow automation guide
```

#### Fun
```
Tell me a joke
Tell me a fact
Make me laugh
```

---

## 🎯 Interface Overview

### Top Section - Header
- **Title**: "✨ MAYA ✨"
- **Subtitle**: "Intelligent Voice AI Assistant"
- Animated effects on startup

### Left Panel - Main Interaction

**Input Section**:
- Text input field
- Send button
- Control buttons (Listen, Clear, Help)
- Quick command suggestions

**Response Section**:
- Large scrollable text area
- Shows Maya's responses with timestamps
- Conversation history maintained
- Color-coded for easy reading

### Right Panel - Status & Info

**System Status Card**:
- Voice system status
- Network connection status
- Memory system status
- API availability (4/4 ready)

**Quick Stats Card**:
- Version information
- Current mode (Web)
- Logged-in user
- Interaction count

**Features Card**:
- Lists all available features
- Quick reference guide

---

## 🔧 Technical Details

### Architecture

```
Web Browser (HTML/CSS/JS)
        ↓
    [Web UI]
        ↓
   Flask Server
        ↓
Python Backend (Brain)
        ↓
APIs, Memory, Voice, Modules
```

### Components

**Frontend** (`maya_web_ui.html`):
- Pure HTML/CSS/JavaScript
- No frameworks (vanilla JS)
- Responsive design
- Unicorn Studio integration

**Backend Server** (`maya_web_server.py`):
- Flask web server
- RESTful API endpoints
- CORS enabled for web requests
- Automatic browser launch

**Integration**:
- Smart Brain processing
- Memory system
- Voice synthesis
- All APIs available

---

## 🌐 API Endpoints

### Process Command
```
POST /api/command
Content-Type: application/json

{
  "message": "What's the weather in London?",
  "speak": false
}

Response:
{
  "success": true,
  "response": "Weather in London: 15°C, Partly Cloudy...",
  "timestamp": "2026-06-14T10:30:45.123"
}
```

### Get Status
```
GET /api/status

Response:
{
  "voice": "ready",
  "network": "online",
  "memory": { ... },
  "apis": {
    "openrouter": true,
    "firecrawl": true,
    "kie_ai": true,
    "openweather": true
  }
}
```

### Get Memory Stats
```
GET /api/memory

Response:
{
  "stats": { ... },
  "interactions": 42,
  "patterns": 15
}
```

### Health Check
```
GET /api/health

Response:
{
  "status": "healthy",
  "service": "Maya AI Assistant",
  "version": "1.0.0",
  "mode": "web"
}
```

---

## 🎨 Customization

### Change Colors

Edit `maya_web_ui.html` and modify these CSS variables:

```css
--primary-color: #00d9ff;  /* Cyan */
--accent-color: #00ffaa;   /* Green */
--success-color: #00ff99;  /* Light Green */
--bg-dark: #0a0e1e;        /* Dark Background */
--bg-card: #0f1428;        /* Card Background */
```

### Modify Background

The Unicorn Studio background is embedded via:
```html
<div data-us-project="K7xzrAoejHe2lHXqTJzm" class="unicorn-background"></div>
```

To change the background:
1. Create a new animation at https://unicorn.studio/
2. Get the project ID
3. Replace `K7xzrAoejHe2lHXqTJzm` with your project ID

### Adjust Layout

The layout is CSS Grid-based and responsive. Modify:
- `.content-wrapper` - Main layout
- `.left-panel` - Input/response area
- `.right-panel` - Status sidebar

---

## 🔌 Requirements

### Python Packages
```
flask
flask-cors
python-dotenv
requests
```

### Browser Requirements
- Modern browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- Minimum resolution: 1024x768
- Optional: Microphone for voice input

### System Requirements
- Python 3.8+
- Virtual environment
- Maya backend properly configured
- .env file with API keys

---

## 🐛 Troubleshooting

### Web Server Won't Start

**Problem**: "Address already in use"
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
# Then restart
bash launch_maya_web.sh
```

### Backend Not Responding

**Problem**: "Could not connect to Maya backend"
```bash
# Ensure server is running
ps aux | grep maya_web_server.py

# Restart if needed
bash launch_maya_web.sh
```

### Voice Recognition Not Working

**Problem**: "Voice recognition not supported"
- Use Chrome, Firefox, or Edge (Safari has limited support)
- Grant microphone permission when prompted
- Check browser console for errors

### Slow Performance

**Problem**: UI is laggy or animations stutter
- Close other browser tabs
- Disable browser extensions
- Update graphics drivers
- Try a different browser

### API Calls Failing

**Problem**: Commands return errors
- Check .env file exists and has valid keys
- Verify network connectivity
- Check server console for error messages
- Review API quotas/limits

---

## 📊 Performance Tips

1. **Browser**: Use Chrome for best performance
2. **Network**: Ensure stable internet connection
3. **Hardware**: Works best on modern computers
4. **Memory**: Close unused applications
5. **Cache**: Clear browser cache if UI is slow

---

## 🔐 Security

### API Keys
- All API keys stored in `.env` file
- Never exposed in frontend code
- CORS enabled for localhost only
- In production, add authentication

### Data Privacy
- Chat history stored locally in browser
- Option to clear history anytime
- No data sent to external services (except configured APIs)
- Memory system uses local JSON file

---

## 📚 Integration with Desktop

### Open Web UI from macOS App

Edit `Maya.app/Contents/MacOS/Maya`:
```bash
# Add after setting up environment:
open http://localhost:5000
python3 maya_web_server.py
```

### Create Desktop Shortcut (macOS)

```bash
# Create launcher app
cp -r Maya.app Maya-Web.app
# Modify the executable to launch web server
```

---

## 🚀 Advanced Usage

### Custom Commands

Add new endpoints to `maya_web_server.py`:

```python
@app.route('/api/custom', methods=['POST'])
def custom_endpoint():
    data = request.get_json()
    # Process data
    return jsonify({'result': 'data'})
```

### Connect Multiple Clients

The server supports multiple web clients:
```
Client 1 (Browser)  ┐
Client 2 (Browser)  ├─→ Flask Server ─→ Python Backend
Client 3 (Browser)  ┘
```

### Extend Status Monitoring

Add real-time updates:
```javascript
// Poll for status changes
setInterval(updateStatus, 5000);
```

---

## 📝 Files Overview

```
/home/user/bp/
├── maya_web_ui.html           # Main web interface
├── maya_web_server.py         # Flask backend server
├── launch_maya_web.sh         # Web server launcher
├── MAYA_WEB_UI.md            # This guide
│
├── Brain/
│   ├── smart_brain.py        # Connected to web API
│   ├── maya_memory.py        # Memory system
│   └── maya_super_powers.py  # APIs (OpenRouter, etc.)
│
└── TextToSpeech/
    └── Fast_DF_TTS.py        # Voice system
```

---

## 🎓 Learning Resources

### JavaScript/HTML/CSS
- Modern web development is used
- No frameworks (vanilla JS)
- ES6+ features
- Responsive design patterns

### Flask
- RESTful API design
- CORS handling
- JSON request/response
- Error handling

### Python Backend
- Smart command routing
- Memory management
- API integrations
- Voice synthesis

---

## 🌟 Features Showcase

### Command Examples

```
User: "What's the weather in Sydney?"
Maya: "🌤️ Weather in Sydney: 22°C, Mostly sunny, Humidity: 60%"

User: "Tell me a joke"
Maya: "Why do programmers prefer dark mode? Because light attracts bugs! 😄"

User: "Analyze machine learning"
Maya: "Machine learning is a subset of AI that uses algorithms to learn patterns from data..."

User: "What's my schedule?"
Maya: "📅 You have 3 meetings today:
1. Team Standup at 10:00
2. Project Review at 14:00
3. 1-on-1 with Manager at 16:00"
```

---

## 🎯 Next Steps

1. **Launch the server**: `bash launch_maya_web.sh`
2. **Test commands**: Try "What can you do?"
3. **Explore features**: Use voice input and get responses
4. **Monitor status**: Check real-time system status
5. **Customize**: Modify colors and background

---

## 📞 Support

If you encounter issues:
1. Check server console for errors
2. Review browser developer console (F12)
3. Verify .env file configuration
4. Ensure all dependencies are installed
5. Check network connectivity

---

## 🎉 Enjoy Maya!

Your Maya Web UI is ready to use. Start the server and experience the beautiful animated interface with all the power of Maya's AI!

```bash
bash /home/user/bp/launch_maya_web.sh
```

**Welcome to the future! 🚀✨**
