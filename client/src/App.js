import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import Dashboard from './components/Dashboard';
import ArticleGrid from './components/ArticleGrid';
import Sidebar from './components/Sidebar';

function App() {
  const [summaries, setSummaries] = useState([]);
  const [stats, setStats] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 3600000); // Refresh hourly
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [summariesRes, statsRes] = await Promise.all([
        axios.get('/api/summaries'),
        axios.get('/api/stats')
      ]);
      setSummaries(summariesRes.data.summaries);
      setStats(statsRes.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch data. Check if server is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredSummaries = selectedCategory
    ? summaries.filter(s => s.category === selectedCategory)
    : summaries;

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>🤖 AI Agent Dashboard</h1>
          <p className="subtitle">Daily Substack summaries on AI skills & multi-agent systems</p>
        </div>
      </header>

      <div className="app-container">
        <Sidebar
          stats={stats}
          selectedCategory={selectedCategory}
          onSelectCategory={setSelectedCategory}
        />

        <main className="main-content">
          {error && (
            <div className="error-banner">
              <span>⚠️ {error}</span>
              <button onClick={fetchData}>Retry</button>
            </div>
          )}

          {loading ? (
            <div className="loading">
              <div className="spinner"></div>
              <p>Loading latest articles...</p>
            </div>
          ) : (
            <>
              {stats && <Dashboard stats={stats} />}
              <ArticleGrid
                articles={filteredSummaries}
                categoryFilter={selectedCategory}
              />
            </>
          )}
        </main>
      </div>

      <footer className="app-footer">
        <p>Updated daily • Powered by Claude AI Agent Orchestration</p>
      </footer>
    </div>
  );
}

export default App;
