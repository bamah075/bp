import React from 'react';
import './Sidebar.css';

function Sidebar({ stats, selectedCategory, onSelectCategory }) {
  const categories = stats?.categories || {};

  return (
    <aside className="sidebar">
      <div className="sidebar-content">
        <h3 className="sidebar-title">Filters</h3>

        <button
          className={`category-filter ${selectedCategory === null ? 'active' : ''}`}
          onClick={() => onSelectCategory(null)}
        >
          <span>All Articles</span>
          <span className="count">{stats?.totalArticles || 0}</span>
        </button>

        {Object.entries(categories).map(([category, count]) => (
          <button
            key={category}
            className={`category-filter ${selectedCategory === category ? 'active' : ''}`}
            onClick={() => onSelectCategory(category)}
          >
            <span>{category}</span>
            <span className="count">{count}</span>
          </button>
        ))}
      </div>

      <div className="sidebar-footer">
        <div className="info-card">
          <h4>About This Dashboard</h4>
          <p>
            Curated daily summaries of AI agent content from Substack, powered by multi-agent orchestration.
          </p>
        </div>

        <div className="agent-info">
          <h4>Agent Architecture</h4>
          <ul>
            <li>📡 Fetcher Agent</li>
            <li>🔍 Analyzer Agent</li>
            <li>📝 Summarizer Agent</li>
            <li>🎯 Orchestrator</li>
          </ul>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
