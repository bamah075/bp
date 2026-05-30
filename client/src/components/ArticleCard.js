import React from 'react';
import './ArticleCard.css';

function ArticleCard({ article, isExpanded, onToggle }) {
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric'
    });
  };

  const getCategoryEmoji = (category) => {
    const emojis = {
      'AI Skills': '🎯',
      'Multi-Agent Systems': '🤖',
      'Dashboard Design': '📊',
      'Agent Architecture': '🏗️',
      'Automation': '⚙️',
      'Engineering': '🛠️'
    };
    return emojis[category] || '📌';
  };

  return (
    <div className={`article-card ${isExpanded ? 'expanded' : ''}`}>
      <div className="card-header">
        <div className="card-meta">
          <span className="category-badge">
            {getCategoryEmoji(article.category)} {article.category}
          </span>
          <span className="date">{formatDate(article.date)}</span>
        </div>
        <button
          className="expand-btn"
          onClick={onToggle}
          aria-label="Toggle expanded view"
        >
          {isExpanded ? '−' : '+'}
        </button>
      </div>

      <h3 className="card-title">{article.title}</h3>
      <p className="publication">{article.publication}</p>
      <p className="summary">{article.summary}</p>

      {isExpanded && (
        <div className="card-expanded">
          {article.keyPoints && (
            <div className="key-points">
              <h4>Key Points:</h4>
              <ul>
                {article.keyPoints.map((point, idx) => (
                  <li key={idx}>{point}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <div className="card-footer">
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="read-btn"
        >
          Read on Substack →
        </a>
      </div>
    </div>
  );
}

export default ArticleCard;
