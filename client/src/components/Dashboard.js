import React from 'react';
import './Dashboard.css';

function Dashboard({ stats }) {
  if (!stats) return null;

  const categoryEntries = Object.entries(stats.categories || {});

  return (
    <div className="dashboard">
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>Total Articles</h3>
            <p className="stat-value">{stats.totalArticles}</p>
            <small>Updated today</small>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🏷️</div>
          <div className="stat-content">
            <h3>Categories</h3>
            <p className="stat-value">{categoryEntries.length}</p>
            <small>Topics covered</small>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⏰</div>
          <div className="stat-content">
            <h3>Last Updated</h3>
            <p className="stat-value">
              {new Date(stats.lastUpdated).toLocaleTimeString()}
            </p>
            <small>Today</small>
          </div>
        </div>
      </div>

      <div className="categories-section">
        <h3>Articles by Category</h3>
        <div className="category-breakdown">
          {categoryEntries.map(([category, count]) => (
            <div key={category} className="category-item">
              <span className="category-name">{category}</span>
              <div className="category-bar-wrapper">
                <div
                  className="category-bar"
                  style={{
                    width: `${(count / stats.totalArticles) * 100}%`
                  }}
                ></div>
              </div>
              <span className="category-count">{count}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
