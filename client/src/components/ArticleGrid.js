import React, { useState } from 'react';
import ArticleCard from './ArticleCard';
import './ArticleGrid.css';

function ArticleGrid({ articles, categoryFilter }) {
  const [expandedId, setExpandedId] = useState(null);

  const toggleExpand = (id) => {
    setExpandedId(expandedId === id ? null : id);
  };

  if (articles.length === 0) {
    return (
      <div className="empty-state">
        <p>No articles found in this category.</p>
      </div>
    );
  }

  return (
    <div className="article-grid">
      <div className="grid-header">
        <h2>
          {categoryFilter ? `${categoryFilter} Articles` : 'Latest Articles'}
        </h2>
        <p className="article-count">{articles.length} articles</p>
      </div>

      <div className="cards-container">
        {articles.map((article) => (
          <ArticleCard
            key={article.id}
            article={article}
            isExpanded={expandedId === article.id}
            onToggle={() => toggleExpand(article.id)}
          />
        ))}
      </div>
    </div>
  );
}

export default ArticleGrid;
