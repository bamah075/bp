# 🤖 Substack AI Agent Dashboard

A sophisticated multi-agent orchestration system that aggregates, analyzes, and summarizes AI agent content from Substack. Features a beautiful React dashboard with real-time updates and intelligent content categorization.

## ✨ Features

- **Multi-Agent Orchestration**: Three specialized Claude agents working in tandem
  - 📡 **Fetcher Agent**: Discovers and aggregates Substack content
  - 🔍 **Analyzer Agent**: Extracts insights and key concepts
  - 📝 **Summarizer Agent**: Creates daily digests and recommendations
  - 🎯 **Orchestrator**: Coordinates all agents

- **Beautiful Dashboard**
  - 🎨 Modern gradient UI with responsive design
  - 📊 Real-time statistics and category breakdowns
  - 🏷️ Smart categorization of articles
  - 🔍 Filter by topic or view all

- **Daily Summaries**
  - Top insights across all articles
  - Trending topics identification
  - Personalized reading recommendations
  - Practical tips for AI agent usage

- **Smart Features**
  - Expandable article cards with key points
  - Direct links to original Substack articles
  - Category-based filtering
  - Hourly automatic refresh

## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- Claude API key (from Anthropic)

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd bp

# Install backend dependencies
npm install

# Install frontend dependencies
cd client && npm install && cd ..

# Set up environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Running Locally

```bash
# Development mode (backend + frontend)
npm run dev

# Or run separately:

# Terminal 1: Backend server (http://localhost:3001)
npm start

# Terminal 2: Frontend development (http://localhost:3000)
cd client && npm start
```

### Running the Agent

```bash
# Fetch and analyze Substack content
npm run agent
```

This executes the multi-agent orchestration pipeline:
1. Fetcher discovers articles
2. Analyzer extracts insights
3. Summarizer creates daily digest
4. Results displayed in dashboard

## 📁 Project Structure

```
/home/user/bp
├── server.js              # Express backend API
├── agent.js               # Multi-agent orchestrator
├── package.json           # Backend dependencies
├── .env.example          # Environment template
│
└── client/
    ├── src/
    │   ├── App.js        # Main React component
    │   ├── App.css       # Global styles
    │   └── components/
    │       ├── Dashboard.js    # Stats component
    │       ├── ArticleGrid.js  # Article list
    │       ├── ArticleCard.js  # Individual article
    │       ├── Sidebar.js      # Filter sidebar
    │       └── [.css files]    # Component styles
    │
    ├── public/
    │   └── index.html    # React root HTML
    │
    └── package.json      # Frontend dependencies
```

## 🔌 API Endpoints

### Get All Summaries
```
GET /api/summaries
Response: { summaries: [...], totalArticles: number, date: string }
```

### Get Summary by ID
```
GET /api/summaries/:id
Response: { id, title, summary, url, category, keyPoints: [...] }
```

### Filter by Category
```
GET /api/categories/:category
Response: { category, count, summaries: [...] }
```

### Dashboard Stats
```
GET /api/stats
Response: { totalArticles, categories: {}, lastUpdated, date }
```

### Health Check
```
GET /api/health
Response: { status: "ok", timestamp }
```

## 🤖 Agent Architecture

### Fetcher Agent
- Searches Substack for AI agent and skill content
- Extracts article metadata
- Returns structured article data

### Analyzer Agent
- Processes fetched articles
- Identifies key technical concepts
- Rates innovation and relevance
- Creates content insights

### Summarizer Agent
- Synthesizes analyzer insights
- Generates top insights
- Identifies trending topics
- Creates reading recommendations
- Produces practical daily tips

### Orchestrator
- Manages agent execution flow
- Coordinates data pipelines
- Aggregates results
- Provides scheduling

## 🎨 Design Features

- **Color Scheme**: Purple gradient (#667eea → #764ba2)
- **Animations**: Smooth transitions and hover effects
- **Responsive**: Works on desktop, tablet, mobile
- **Accessibility**: Semantic HTML, proper ARIA labels

## 📊 Dashboard Components

### Stats Cards
- Total articles count
- Category breakdown
- Last update timestamp

### Category Breakdown
- Visual bar charts
- Article count per category
- Real-time filtering

### Article Cards
- Expandable details
- Category badges with emojis
- Direct Substack links
- Key points summary

### Sidebar
- Category filters
- Agent architecture info
- Dashboard description

## 🔧 Configuration

### Environment Variables
```env
ANTHROPIC_API_KEY=your-api-key       # Required for Claude API
PORT=3001                            # Server port
NODE_ENV=development                 # Environment
FETCH_INTERVAL=3600000              # Refresh interval (ms)
```

### Customization

**Add new categories**: Edit `agent.js` search queries
```javascript
const queries = [
  'AI agents skills Substack',
  'your-new-query-here',
];
```

**Change colors**: Update CSS gradients in component files
```css
background: linear-gradient(135deg, #your-color1 0%, #your-color2 100%);
```

**Modify refresh rate**: Update `App.js` interval
```javascript
const interval = setInterval(fetchData, 3600000); // Change timing
```

## 📦 Build & Deploy

### Build Frontend
```bash
cd client
npm run build
```

Output in `client/build/` ready for deployment.

### Build Docker Image (Optional)
```bash
docker build -t substack-dashboard .
docker run -p 3001:3001 -e ANTHROPIC_API_KEY=your-key substack-dashboard
```

## 🧪 Testing

```bash
# Frontend tests
cd client && npm test

# Backend health check
curl http://localhost:3001/api/health
```

## 📈 Future Enhancements

- [ ] Database persistence (PostgreSQL)
- [ ] User authentication
- [ ] Scheduled daily emails
- [ ] Advanced filtering (date range, authors)
- [ ] Share and export summaries
- [ ] Dark mode toggle
- [ ] Saved articles / reading list
- [ ] Custom agent configurations

## 🛠️ Troubleshooting

### "Cannot find module 'express'"
```bash
npm install
cd client && npm install && cd ..
```

### API returning sample data
The server includes fallback sample data. To use real Substack data:
1. Set `ANTHROPIC_API_KEY` in `.env`
2. Implement RSS feed integration or web scraping
3. Update `server.js` fetch logic

### Port 3001 already in use
```bash
# Use different port
PORT=3002 npm start
```

## 📝 License

MIT License - feel free to modify and deploy

## 🤝 Contributing

Contributions welcome! Areas:
- Substack RSS feed integration
- Additional agent types
- UI enhancements
- Database integration
- Tests and documentation

## 📧 Support

For issues or questions:
1. Check API responses in browser DevTools
2. Review server logs for agent execution
3. Verify `.env` configuration
4. Check Claude API quota

---

**Built with Claude API • Powered by Multi-Agent Orchestration**
