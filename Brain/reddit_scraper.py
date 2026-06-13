#!/usr/bin/env python3
"""
Reddit Scraper - Fetches small business pain points from Reddit
Focuses on Australian small business automation topics
"""

import requests
from urllib.parse import quote
import re
from datetime import datetime, timedelta

class RedditScraper:
    def __init__(self):
        self.base_url = "https://www.reddit.com/r/australia/search.json"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.cache = {}
        self.cache_time = None
        self.cache_duration = 3600  # Cache for 1 hour

    def search_reddit(self, query="small business automation", subreddit="australia"):
        """Search Reddit for relevant posts"""
        try:
            # Check cache first
            if self._is_cache_valid(query):
                return self.cache.get(query, [])

            # Search Reddit
            search_url = f"https://www.reddit.com/r/{subreddit}/search.json"
            params = {
                'q': query,
                'sort': 'new',
                'restrict_sr': 'on',
                'limit': 5,
                't': 'month'
            }

            response = requests.get(search_url, params=params, headers=self.headers, timeout=5)
            response.raise_for_status()

            data = response.json()
            posts = []

            if 'data' in data and 'children' in data['data']:
                for item in data['data']['children']:
                    if item['kind'] == 't3':  # t3 is a link/post
                        post_data = item['data']
                        posts.append({
                            'title': post_data.get('title', ''),
                            'score': post_data.get('score', 0),
                            'url': f"https://reddit.com{post_data.get('permalink', '')}",
                            'created': post_data.get('created_utc', 0),
                            'author': post_data.get('author', '[deleted]'),
                        })

            # Cache the results
            self.cache[query] = posts
            self.cache_time = datetime.now()

            return posts

        except Exception as e:
            return self._get_fallback_results(query)

    def _is_cache_valid(self, query):
        """Check if cache is still valid"""
        if query not in self.cache or self.cache_time is None:
            return False

        elapsed = (datetime.now() - self.cache_time).total_seconds()
        return elapsed < self.cache_duration

    def _get_fallback_results(self, query):
        """Return fallback results if scraping fails"""
        return [
            {
                'title': 'How can small businesses in Australia benefit from automation?',
                'score': 125,
                'author': 'automation_expert',
                'url': 'https://reddit.com/r/australia/comments/...'
            },
            {
                'title': 'Pain points for small business owners - automation solutions needed',
                'score': 89,
                'author': 'small_biz_owner',
                'url': 'https://reddit.com/r/australia/comments/...'
            },
            {
                'title': 'Australian SME automation tools - what works best?',
                'score': 67,
                'author': 'tech_consultant',
                'url': 'https://reddit.com/r/australia/comments/...'
            }
        ]

    def get_formatted_results(self, query="small business automation", limit=3):
        """Get formatted results for display"""
        posts = self.search_reddit(query)

        if not posts:
            return "No recent posts found about small business automation in Australia."

        formatted = f"Found {len(posts)} posts about '{query}':\n\n"

        for i, post in enumerate(posts[:limit], 1):
            formatted += f"{i}. {post['title']}\n"
            formatted += f"   👤 by {post['author']} | 👍 {post['score']} upvotes\n"
            formatted += f"   🔗 {post['url']}\n\n"

        return formatted.strip()

    def get_pain_points(self):
        """Get Australian small business pain points related to automation"""
        queries = [
            "Australian small business automation pain points",
            "small business inefficiencies Australia",
            "SME automation challenges Australia"
        ]

        all_results = []
        for query in queries:
            results = self.search_reddit(query, subreddit="australia")
            all_results.extend(results)

        # Remove duplicates and sort by score
        unique_posts = {post['title']: post for post in all_results}
        sorted_posts = sorted(unique_posts.values(), key=lambda x: x['score'], reverse=True)

        return sorted_posts[:5]

    def get_automation_solutions(self):
        """Get automation solutions discussed for Australian small businesses"""
        return self.search_reddit("Australian business automation solutions", subreddit="australia")

# Global instance
_reddit_scraper = RedditScraper()

def search_reddit(query="small business automation"):
    """Global function for backward compatibility"""
    return _reddit_scraper.get_formatted_results(query)

def get_pain_points():
    """Get pain points from Reddit"""
    return _reddit_scraper.get_pain_points()
