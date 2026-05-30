const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// In-memory storage for daily summaries (in production, use a database)
let dailySummaries = [];
let lastFetchTime = null;

// Simulated data structure
const sampleData = {
  date: new Date().toISOString().split('T')[0],
  summaries: [
    {
      id: 1,
      title: "Claude AI Skill: Run a Standup Meeting",
      publication: "AI Skill of the Week",
      summary: "Learn how to use Claude to automate and run effective standup meetings with AI agents.",
      url: "https://www.aiskilloftheweek.com/p/claude-ai-skill-run-a-standup-meeting",
      category: "AI Skills",
      date: new Date().toISOString(),
      keyPoints: [
        "Automate meeting notes with Claude",
        "Generate action items automatically",
        "Multi-agent orchestration for team updates"
      ]
    },
    {
      id: 2,
      title: "Multi-Agent Orchestration Patterns",
      publication: "Agent Engineering Digest",
      summary: "Explore advanced patterns for coordinating multiple AI agents in complex workflows.",
      url: "https://example.com/multi-agent-patterns",
      category: "Multi-Agent Systems",
      date: new Date().toISOString(),
      keyPoints: [
        "Supervisor agents for task delegation",
        "Tool use between agents",
        "Error handling in multi-agent systems"
      ]
    },
    {
      id: 3,
      title: "Building Autonomous Agent Dashboards",
      publication: "Agent Architecture Weekly",
      summary: "Design patterns for creating dashboards that monitor and control autonomous agents.",
      url: "https://example.com/agent-dashboards",
      category: "Dashboard Design",
      date: new Date().toISOString(),
      keyPoints: [
        "Real-time agent monitoring",
        "Performance metrics visualization",
        "Intervention and control interfaces"
      ]
    }
  ]
};

// API Routes

// Get all daily summaries
app.get('/api/summaries', (req, res) => {
  res.json({
    success: true,
    date: new Date().toISOString().split('T')[0],
    totalArticles: sampleData.summaries.length,
    summaries: sampleData.summaries
  });
});

// Get summary by ID
app.get('/api/summaries/:id', (req, res) => {
  const summary = sampleData.summaries.find(s => s.id === parseInt(req.params.id));
  if (!summary) {
    return res.status(404).json({ error: 'Summary not found' });
  }
  res.json(summary);
});

// Get summaries by category
app.get('/api/categories/:category', (req, res) => {
  const filtered = sampleData.summaries.filter(
    s => s.category.toLowerCase() === req.params.category.toLowerCase()
  );
  res.json({
    category: req.params.category,
    count: filtered.length,
    summaries: filtered
  });
});

// Get dashboard stats
app.get('/api/stats', (req, res) => {
  const categories = {};
  sampleData.summaries.forEach(s => {
    categories[s.category] = (categories[s.category] || 0) + 1;
  });

  res.json({
    totalArticles: sampleData.summaries.length,
    categories: categories,
    lastUpdated: lastFetchTime || new Date().toISOString(),
    date: new Date().toISOString().split('T')[0]
  });
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Serve static files from client build
app.use(express.static(path.join(__dirname, 'client/build')));

// Fallback to index.html for React routing
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'client/build/index.html'));
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
