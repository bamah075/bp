#!/usr/bin/env python3
"""
Analyzer for r/ausbusiness pain points.
Loads sample data and groups pain points by category.
"""

import json
import re
from collections import defaultdict
from datetime import datetime

def load_sample_data(filename='sample_data.json'):
    """Load sample Reddit posts data."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return None

def categorize_pain_points():
    """Define pain point categories and keywords."""
    return {
        'Compliance & Regulations': {
            'keywords': [
                'abn', 'ato', 'gst', 'payg', 'tax', 'compliance', 'regulation',
                'legal', 'audit', 'workplace relations', 'modern awards',
                'unfair dismissal', 'super', 'superannuation', 'privacy',
                'occupational health', 'licensing', 'federal', 'state'
            ],
            'description': 'Complex regulations, tax requirements, workplace laws'
        },
        'Cash Flow & Finance': {
            'keywords': [
                'cash flow', 'payment', 'invoice', 'outstanding', 'debt', 'loan',
                'interest rate', 'funding', 'capital', 'profit margin', 'bank',
                'credit', 'afford', 'expensive', 'cost', 'expensive', 'finance',
                'bootstrap', 'collateral'
            ],
            'description': 'Payment delays, loan access, interest rates, profitability'
        },
        'Staffing & HR': {
            'keywords': [
                'employee', 'staff', 'hire', 'recruitment', 'retention', 'turnover',
                'wage', 'salary', 'payroll', 'hr', 'training', 'skill shortage',
                'workers', 'casual', 'permanent', 'bonus', 'loyalty'
            ],
            'description': 'Hiring challenges, retention, training costs, wage pressures'
        },
        'Marketing & Sales': {
            'keywords': [
                'customer', 'sales', 'marketing', 'advertising', 'competition',
                'competitors', 'pricing', 'acquisition', 'roi', 'reach',
                'ads', 'google', 'facebook', 'organic', 'budget', 'growth'
            ],
            'description': 'Customer acquisition, competition, advertising costs'
        },
        'Technology & Systems': {
            'keywords': [
                'technology', 'software', 'digital', 'automation', 'cyber',
                'security', 'data', 'integration', 'online', 'platform', 'app',
                'website', 'cloud', 'legacy', 'saas', 'ransomware', 'breach'
            ],
            'description': 'Digital infrastructure, cybersecurity, legacy systems'
        },
        'Supply Chain & Operations': {
            'keywords': [
                'supplier', 'supply chain', 'inventory', 'shipping', 'delivery',
                'logistics', 'production', 'operations', 'freight', 'disruption',
                'material', 'quality', 'lead time', 'waste', 'efficiency'
            ],
            'description': 'Supplier reliability, logistics, inventory management'
        },
        'Real Estate & Facilities': {
            'keywords': [
                'rent', 'lease', 'commercial', 'location', 'office', 'regional',
                'urban', 'space', 'property', 'facility', 'moving'
            ],
            'description': 'Rising rents, location challenges, facility costs'
        },
        'Market & Economic': {
            'keywords': [
                'economy', 'market', 'inflation', 'recession', 'dollar',
                'cost of living', 'consumer', 'demand', 'trends', 'commodity',
                'international', 'amazon', 'china', 'competing'
            ],
            'description': 'Economic pressures, market competition, pricing pressure'
        }
    }

def extract_pain_points(text, categories):
    """Extract pain points from text based on keyword matching."""
    if not text:
        return {}

    text_lower = text.lower()
    found_categories = {}

    for category, info in categories.items():
        for keyword in info['keywords']:
            if keyword in text_lower:
                if category not in found_categories:
                    found_categories[category] = []
                if keyword not in found_categories[category]:
                    found_categories[category].append(keyword)

    return found_categories

def analyze_posts(data, categories):
    """Analyze all posts and group pain points."""
    if not data or 'posts' not in data:
        return None

    posts = data['posts']
    pain_points_by_category = defaultdict(lambda: {'keywords': set(), 'posts': [], 'count': 0})
    detailed_posts = []

    for post in posts:
        title = post.get('title', '')
        selftext = post.get('selftext', '')
        author = post.get('author', '')
        upvotes = post.get('upvotes', 0)
        post_id = post.get('id', '')

        # Combine title and text for analysis
        full_text = f"{title} {selftext}"

        # Extract pain points
        found_categories = extract_pain_points(full_text, categories)

        if found_categories:
            post_info = {
                'id': post_id,
                'title': title,
                'author': author,
                'upvotes': upvotes,
                'categories': list(found_categories.keys()),
                'keywords': {cat: keywords for cat, keywords in found_categories.items()}
            }
            detailed_posts.append(post_info)

            # Aggregate by category
            for category, keywords in found_categories.items():
                pain_points_by_category[category]['keywords'].update(keywords)
                pain_points_by_category[category]['posts'].append(post_id)
                pain_points_by_category[category]['count'] += 1

    # Convert sets to sorted lists
    aggregated = {
        category: {
            'description': categories[category]['description'],
            'keywords': sorted(list(info['keywords'])),
            'mention_count': len(info['posts']),
            'post_ids': info['posts']
        }
        for category, info in pain_points_by_category.items()
    }

    return {
        'timestamp': datetime.now().isoformat(),
        'total_posts': len(posts),
        'posts_with_pain_points': len(detailed_posts),
        'categories': aggregated,
        'detailed_posts': detailed_posts
    }

def save_results(analysis, filename='pain_points_analysis.json'):
    """Save analysis results to JSON."""
    with open(filename, 'w') as f:
        json.dump(analysis, f, indent=2)
    print(f"✓ Results saved to {filename}")

def print_summary(analysis, categories):
    """Print a formatted summary of findings."""
    print("\n" + "="*70)
    print("AUSTRALIAN BUSINESS PAIN POINTS ANALYSIS")
    print("r/ausbusiness Subreddit")
    print("="*70)
    print(f"\nAnalysis Date: {analysis['timestamp']}")
    print(f"Posts Analyzed: {analysis['total_posts']}")
    print(f"Posts with Identified Pain Points: {analysis['posts_with_pain_points']}")
    print(f"Coverage: {(analysis['posts_with_pain_points']/analysis['total_posts']*100):.1f}%")

    print("\n" + "-"*70)
    print("PAIN POINTS BY CATEGORY")
    print("-"*70)

    # Sort by mention count
    sorted_categories = sorted(
        analysis['categories'].items(),
        key=lambda x: x[1]['mention_count'],
        reverse=True
    )

    for category, data in sorted_categories:
        print(f"\n{category}")
        print(f"  Description: {data['description']}")
        print(f"  Mentioned in: {data['mention_count']} posts")
        print(f"  Key Issues: {', '.join(data['keywords'][:5])}")
        if len(data['keywords']) > 5:
            print(f"               and {len(data['keywords']) - 5} more...")

    print("\n" + "-"*70)
    print("TOP AFFECTED POSTS (by engagement)")
    print("-"*70)

    # Sort posts by upvotes
    sorted_posts = sorted(
        analysis['detailed_posts'],
        key=lambda x: x['upvotes'],
        reverse=True
    )[:5]

    for i, post in enumerate(sorted_posts, 1):
        print(f"\n{i}. {post['title']}")
        print(f"   Upvotes: {post['upvotes']} | Categories: {', '.join(post['categories'])}")

def main():
    print("Loading sample data...")
    data = load_sample_data('sample_data.json')

    if not data:
        return

    print("Analyzing pain points...")
    categories = categorize_pain_points()
    analysis = analyze_posts(data, categories)

    if analysis:
        save_results(analysis)
        print_summary(analysis, categories)

        print("\n" + "="*70)
        print("Analysis complete! Full results saved to pain_points_analysis.json")
        print("="*70 + "\n")
    else:
        print("Failed to analyze data.")

if __name__ == "__main__":
    main()
