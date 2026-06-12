#!/usr/bin/env python3
"""
Scraper for r/ausbusiness subreddit to extract and group pain points.
"""

import json
import re
import requests
from collections import defaultdict
from datetime import datetime

def fetch_reddit_posts(subreddit="ausbusiness", limit=100):
    """
    Fetch posts from a subreddit using Reddit's JSON API.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Reddit data: {e}")
        return None

def extract_pain_points(text):
    """
    Extract potential pain points from text using keyword matching.
    """
    if not text:
        return []

    pain_point_keywords = {
        'Compliance & Regulations': [
            'regulation', 'compliance', 'abn', 'tax', 'ato', 'legal', 'audit',
            'legislation', 'rules', 'requirements', 'bureaucracy', 'red tape',
            'gst', 'payg', 'superannuation', 'workplace law'
        ],
        'Cash Flow & Finance': [
            'cash flow', 'payment', 'invoice', 'outstanding', 'debt', 'loan',
            'interest rate', 'funding', 'capital', 'money', 'finance', 'bank',
            'credit', 'costly', 'expensive', 'afford', 'budget', 'profit margin'
        ],
        'Staffing & HR': [
            'employee', 'staff', 'hire', 'recruitment', 'retention', 'turnover',
            'wage', 'salary', 'payroll', 'hr', 'human resources', 'training',
            'skill shortage', 'work agreement', 'employment'
        ],
        'Marketing & Sales': [
            'customer', 'sales', 'marketing', 'advertising', 'client', 'market',
            'competition', 'competitors', 'pricing', 'brand', 'visibility',
            'lead', 'conversion', 'reach', 'growth'
        ],
        'Technology & Systems': [
            'technology', 'software', 'system', 'digital', 'automation', 'it',
            'cyber', 'security', 'data', 'integration', 'online', 'platform',
            'app', 'website', 'cloud'
        ],
        'Supply Chain & Operations': [
            'supplier', 'supply chain', 'inventory', 'shipping', 'delivery',
            'logistics', 'production', 'operations', 'cost', 'efficiency',
            'waste', 'process'
        ],
        'Market & Economy': [
            'economy', 'market', 'inflation', 'recession', 'interest rate',
            'dollar', 'cost of living', 'consumer', 'demand', 'trends',
            'commodity', 'prices'
        ],
        'Customer Service': [
            'customer service', 'support', 'complaint', 'satisfaction',
            'feedback', 'experience', 'retention', 'loyalty', 'review'
        ]
    }

    text_lower = text.lower()
    found_points = defaultdict(list)

    for category, keywords in pain_point_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                found_points[category].append(keyword)

    return found_points

def analyze_content(data):
    """
    Analyze Reddit posts and comments to extract and group pain points.
    """
    if not data:
        return None

    pain_points_by_category = defaultdict(set)
    pain_points_by_post = []

    posts = data.get('data', {}).get('children', [])

    for post_item in posts:
        post = post_item.get('data', {})
        title = post.get('title', '')
        selftext = post.get('selftext', '')
        author = post.get('author', 'Unknown')
        score = post.get('score', 0)
        url = post.get('url', '')

        # Combine title and text for analysis
        full_text = f"{title} {selftext}"

        pain_points = extract_pain_points(full_text)

        if pain_points:
            post_info = {
                'title': title,
                'author': author,
                'score': score,
                'url': f"https://reddit.com{post.get('permalink', '')}",
                'categories': dict(pain_points)
            }
            pain_points_by_post.append(post_info)

            # Aggregate by category
            for category, keywords in pain_points.items():
                for keyword in keywords:
                    pain_points_by_category[category].add(keyword)

    return {
        'timestamp': datetime.now().isoformat(),
        'posts_analyzed': len(posts),
        'posts_with_pain_points': len(pain_points_by_post),
        'pain_points_by_category': {
            category: sorted(list(keywords))
            for category, keywords in pain_points_by_category.items()
        },
        'detailed_posts': pain_points_by_post
    }

def save_results(data, filename='pain_points_analysis.json'):
    """
    Save analysis results to a JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Results saved to {filename}")

def main():
    print("Fetching r/ausbusiness posts...")
    reddit_data = fetch_reddit_posts(limit=100)

    if reddit_data:
        print("Analyzing pain points...")
        analysis = analyze_content(reddit_data)

        if analysis:
            save_results(analysis)

            # Print summary
            print("\n" + "="*60)
            print("PAIN POINTS ANALYSIS - r/ausbusiness")
            print("="*60)
            print(f"Posts analyzed: {analysis['posts_analyzed']}")
            print(f"Posts with identified pain points: {analysis['posts_with_pain_points']}")
            print("\nPain Points by Category:")
            print("-"*60)

            for category, keywords in analysis['pain_points_by_category'].items():
                print(f"\n{category}:")
                for keyword in sorted(keywords):
                    print(f"  - {keyword}")
    else:
        print("Failed to fetch data from Reddit.")

if __name__ == "__main__":
    main()
