#!/usr/bin/env python3
"""
Reddit Business Pain Points Scraper
Scrapes business-related subreddits for pain points and classifies them by industry.
"""

import json
import re
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple
import os
import praw

# Industry keywords for classification
INDUSTRY_KEYWORDS = {
    "Healthcare": [
        "patient", "healthcare", "medical", "hospital", "clinic", "pharmacy",
        "doctor", "nurse", "treatment", "diagnosis", "health", "insurance",
        "telemedicine", "ehr", "electronic health record", "physician"
    ],
    "Finance": [
        "bank", "finance", "financial", "investment", "stock", "trading",
        "crypto", "cryptocurrency", "bitcoin", "loan", "mortgage", "payment",
        "accounting", "tax", "revenue", "profit", "cash flow", "budget"
    ],
    "Technology": [
        "software", "tech", "developer", "coding", "programming", "saas",
        "cloud", "api", "database", "infrastructure", "devops", "cybersecurity",
        "ai", "machine learning", "web development", "mobile app", "startup"
    ],
    "Retail": [
        "retail", "ecommerce", "store", "inventory", "customer service",
        "pos", "shopping", "product", "sales", "warehouse", "supply chain",
        "wholesale", "distribution"
    ],
    "Manufacturing": [
        "manufacturing", "production", "factory", "equipment", "supply chain",
        "logistics", "quality control", "automation", "assembly", "warehouse",
        "industrial", "machinery"
    ],
    "Real Estate": [
        "real estate", "property", "landlord", "tenant", "lease", "mortgage",
        "construction", "building", "rent", "apartment", "commercial property",
        "developer", "property management"
    ],
    "HR & Recruitment": [
        "hiring", "recruitment", "employee", "hr", "human resources", "management",
        "payroll", "benefits", "talent", "onboarding", "training", "culture",
        "retention", "compensation"
    ],
    "Marketing": [
        "marketing", "advertising", "brand", "content", "social media", "seo",
        "campaign", "customer acquisition", "conversion", "analytics", "lead",
        "promotion", "engagement"
    ],
    "Education": [
        "education", "school", "university", "student", "teacher", "learning",
        "tuition", "course", "training", "curriculum", "edtech", "enrollment",
        "academic"
    ],
    "Hospitality": [
        "hotel", "restaurant", "hospitality", "tourism", "travel", "catering",
        "dining", "booking", "guest", "reservation", "food service", "venue"
    ]
}

# Subreddits to scrape
SUBREDDITS = [
    "business",
    "entrepreneur",
    "startup",
    "smallbusiness",
    "bizapps",
]

class RedditPainPointsScraper:
    """Scrapes and classifies business pain points from Reddit."""

    def __init__(self, output_file="pain_points_by_industry.json"):
        self.output_file = output_file
        self.pain_points_by_industry = defaultdict(list)
        self.reddit = None

    def authenticate_reddit(self):
        """Authenticate with Reddit API using environment variables."""
        reddit_id = os.getenv("REDDIT_CLIENT_ID")
        reddit_secret = os.getenv("REDDIT_CLIENT_SECRET")
        reddit_user_agent = os.getenv("REDDIT_USER_AGENT", "pain-points-scraper/1.0")

        if not reddit_id or not reddit_secret:
            print("Error: REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables required")
            print("Get credentials from: https://www.reddit.com/prefs/apps")
            return False

        try:
            self.reddit = praw.Reddit(
                client_id=reddit_id,
                client_secret=reddit_secret,
                user_agent=reddit_user_agent
            )
            return True
        except Exception as e:
            print(f"Failed to authenticate with Reddit: {e}")
            return False

    def classify_industry(self, text: str) -> List[str]:
        """Classify text into relevant industries based on keywords."""
        text_lower = text.lower()
        classified_industries = []

        for industry, keywords in INDUSTRY_KEYWORDS.items():
            if any(keyword in text_lower for keyword in keywords):
                classified_industries.append(industry)

        if not classified_industries:
            classified_industries = ["General Business"]

        return classified_industries

    def extract_pain_points(self, text: str) -> List[str]:
        """Extract pain point statements from text."""
        pain_keywords = [
            r"problem[s]?.*?[\.\!?]",
            r"challenge[s]?.*?[\.\!?]",
            r"struggle[s]?.*?[\.\!?]",
            r"difficult.*?[\.\!?]",
            r"issue[s]?.*?[\.\!?]",
            r"pain.*?[\.\!?]",
            r"frustrated.*?[\.\!?]",
            r"struggling.*?[\.\!?]",
            r"difficult.*?[\.\!?]",
        ]

        sentences = text.split('.')
        pain_points = []

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:  # Filter short sentences
                for pattern in pain_keywords:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        pain_points.append(sentence)
                        break

        return pain_points[:3]  # Limit to 3 pain points per post

    def scrape_subreddit(self, subreddit_name: str, limit: int = 50) -> None:
        """Scrape posts from a specific subreddit."""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            print(f"Scraping r/{subreddit_name}...")

            for post in subreddit.hot(limit=limit):
                if post.stickied:  # Skip pinned posts
                    continue

                text = f"{post.title} {post.selftext}"

                # Extract pain points
                pain_points = self.extract_pain_points(text)
                if not pain_points:
                    continue

                # Classify industries
                industries = self.classify_industry(text)

                # Store pain points by industry
                for industry in industries:
                    for pain_point in pain_points:
                        self.pain_points_by_industry[industry].append({
                            "pain_point": pain_point,
                            "source": f"https://reddit.com{post.permalink}",
                            "score": post.score,
                            "timestamp": datetime.fromtimestamp(post.created_utc).isoformat()
                        })

                print(f"  Found {len(pain_points)} pain point(s) for: {post.title[:60]}...")

        except Exception as e:
            print(f"Error scraping r/{subreddit_name}: {e}")

    def scrape_all(self, limit_per_subreddit: int = 50) -> None:
        """Scrape all configured subreddits."""
        if not self.authenticate_reddit():
            return

        for subreddit in SUBREDDITS:
            self.scrape_subreddit(subreddit, limit=limit_per_subreddit)

    def deduplicate_pain_points(self) -> None:
        """Remove duplicate pain points within each industry."""
        for industry in self.pain_points_by_industry:
            seen = set()
            unique_points = []

            for point_obj in self.pain_points_by_industry[industry]:
                # Normalize text for comparison
                normalized = point_obj["pain_point"].lower().strip()

                if normalized not in seen:
                    seen.add(normalized)
                    unique_points.append(point_obj)

            self.pain_points_by_industry[industry] = unique_points

    def save_results(self) -> None:
        """Save results to JSON file."""
        output_data = {
            "generated_at": datetime.now().isoformat(),
            "total_industries": len(self.pain_points_by_industry),
            "total_pain_points": sum(len(points) for points in self.pain_points_by_industry.values()),
            "industries": {}
        }

        for industry in sorted(self.pain_points_by_industry.keys()):
            points = self.pain_points_by_industry[industry]
            output_data["industries"][industry] = {
                "count": len(points),
                "pain_points": points
            }

        with open(self.output_file, 'w') as f:
            json.dump(output_data, f, indent=2)

        print(f"\nResults saved to {self.output_file}")

    def print_summary(self) -> None:
        """Print a summary of findings."""
        print("\n" + "="*60)
        print("BUSINESS PAIN POINTS BY INDUSTRY")
        print("="*60)

        for industry in sorted(self.pain_points_by_industry.keys()):
            points = self.pain_points_by_industry[industry]
            print(f"\n{industry} ({len(points)} pain points)")
            print("-" * 40)

            for i, point_obj in enumerate(points[:5], 1):  # Show top 5
                pain_point = point_obj["pain_point"][:100]
                print(f"{i}. {pain_point}")
                print(f"   Score: {point_obj['score']} | {point_obj['timestamp'][:10]}")

def main():
    """Main entry point."""
    scraper = RedditPainPointsScraper()

    print("Starting Reddit Business Pain Points Scraper...")
    print("This will scrape Reddit and classify pain points by industry.\n")

    scraper.scrape_all(limit_per_subreddit=50)
    scraper.deduplicate_pain_points()
    scraper.save_results()
    scraper.print_summary()

if __name__ == "__main__":
    main()
