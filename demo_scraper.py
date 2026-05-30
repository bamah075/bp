#!/usr/bin/env python3
"""
Demo version of Reddit Business Pain Points Scraper
Uses sample data instead of requiring Reddit API credentials.
"""

import json
from datetime import datetime
from collections import defaultdict
from typing import List

# Sample Reddit posts for demonstration
SAMPLE_POSTS = [
    {
        "title": "Managing patient records is a nightmare",
        "text": "We struggle with HIPAA compliance and our EHR system is outdated. The challenge of integrating multiple hospital systems is becoming increasingly difficult.",
        "score": 245,
        "url": "https://reddit.com/r/healthcare"
    },
    {
        "title": "Inventory management kills our margins",
        "text": "Our retail store has serious issues with inventory tracking. The problem is that our supply chain is fragmented across multiple vendors.",
        "score": 156,
        "url": "https://reddit.com/r/retail"
    },
    {
        "title": "API integration nightmare in our SaaS product",
        "text": "We're struggling with database scaling as our cloud infrastructure grows. The challenge of maintaining API consistency is painful.",
        "score": 423,
        "url": "https://reddit.com/r/technology"
    },
    {
        "title": "Hiring talent is impossible in tech",
        "text": "Our company struggles to find qualified developers. The problem of retaining talent with competitive salaries is draining our budget.",
        "score": 312,
        "url": "https://reddit.com/r/startup"
    },
    {
        "title": "Marketing ROI tracking is broken",
        "text": "We have issues tracking customer acquisition costs across channels. The challenge of attribution modeling is frustrating our team.",
        "score": 187,
        "url": "https://reddit.com/r/marketing"
    },
    {
        "title": "Manufacturing production bottlenecks",
        "text": "Our factory faces difficulties with quality control and automated assembly lines. The problem is that our supply chain logistics are inefficient.",
        "score": 98,
        "url": "https://reddit.com/r/manufacturing"
    },
    {
        "title": "Real estate property management headaches",
        "text": "We struggle with tenant management and maintenance requests. The challenge of collecting rent on time is a constant issue.",
        "score": 134,
        "url": "https://reddit.com/r/realestate"
    },
    {
        "title": "Financial compliance is killing our startup",
        "text": "Banking integrations are problematic and accounting is a nightmare. We're struggling with tax compliance and financial reporting.",
        "score": 267,
        "url": "https://reddit.com/r/finance"
    },
    {
        "title": "Hotel booking system failures",
        "text": "Our hospitality business has problems with reservation systems. The challenge of managing guest requests and staff coordination is painful.",
        "score": 156,
        "url": "https://reddit.com/r/hospitality"
    },
    {
        "title": "Student enrollment and course management issues",
        "text": "Our educational institution struggles with tuition collection and curriculum management. The problem is integrating learning management systems.",
        "score": 89,
        "url": "https://reddit.com/r/education"
    },
]

# Industry keywords for classification
INDUSTRY_KEYWORDS = {
    "Healthcare": [
        "patient", "healthcare", "medical", "hospital", "clinic", "pharmacy",
        "doctor", "nurse", "treatment", "diagnosis", "health", "insurance",
        "telemedicine", "ehr", "electronic health record", "physician", "hipaa"
    ],
    "Finance": [
        "bank", "finance", "financial", "investment", "stock", "trading",
        "crypto", "cryptocurrency", "bitcoin", "loan", "mortgage", "payment",
        "accounting", "tax", "revenue", "profit", "cash flow", "budget", "compliance"
    ],
    "Technology": [
        "software", "tech", "developer", "coding", "programming", "saas",
        "cloud", "api", "database", "infrastructure", "devops", "cybersecurity",
        "ai", "machine learning", "web development", "mobile app", "startup", "scaling"
    ],
    "Retail": [
        "retail", "ecommerce", "store", "inventory", "customer service",
        "pos", "shopping", "product", "sales", "warehouse", "supply chain",
        "wholesale", "distribution", "vendor", "margins"
    ],
    "Manufacturing": [
        "manufacturing", "production", "factory", "equipment", "supply chain",
        "logistics", "quality control", "automation", "assembly", "warehouse",
        "industrial", "machinery", "bottleneck"
    ],
    "Real Estate": [
        "real estate", "property", "landlord", "tenant", "lease", "mortgage",
        "construction", "building", "rent", "apartment", "commercial property",
        "developer", "property management", "maintenance"
    ],
    "HR & Recruitment": [
        "hiring", "recruitment", "employee", "hr", "human resources", "management",
        "payroll", "benefits", "talent", "onboarding", "training", "culture",
        "retention", "compensation", "developer", "qualified"
    ],
    "Marketing": [
        "marketing", "advertising", "brand", "content", "social media", "seo",
        "campaign", "customer acquisition", "conversion", "analytics", "lead",
        "promotion", "engagement", "roi", "attribution"
    ],
    "Education": [
        "education", "school", "university", "student", "teacher", "learning",
        "tuition", "course", "training", "curriculum", "edtech", "enrollment",
        "academic", "learning management"
    ],
    "Hospitality": [
        "hotel", "restaurant", "hospitality", "tourism", "travel", "catering",
        "dining", "booking", "guest", "reservation", "food service", "venue", "staff"
    ]
}

class DemoPainPointsScraper:
    """Demo version using sample data instead of Reddit API."""

    def __init__(self, output_file="pain_points_by_industry.json"):
        self.output_file = output_file
        self.pain_points_by_industry = defaultdict(list)

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
        import re
        pain_keywords = [
            r"problem[s]?.*?(?=\.|$)",
            r"challenge[s]?.*?(?=\.|$)",
            r"struggle[s]?.*?(?=\.|$)",
            r"difficult.*?(?=\.|$)",
            r"issue[s]?.*?(?=\.|$)",
            r"pain.*?(?=\.|$)",
            r"frustrated.*?(?=\.|$)",
            r"nightmare.*?(?=\.|$)",
        ]

        sentences = text.split('.')
        pain_points = []

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:
                for pattern in pain_keywords:
                    if re.search(pattern, sentence, re.IGNORECASE):
                        pain_points.append(sentence)
                        break

        return pain_points[:3]

    def process_sample_data(self) -> None:
        """Process sample data."""
        for post in SAMPLE_POSTS:
            text = f"{post['title']} {post['text']}"

            pain_points = self.extract_pain_points(text)
            if not pain_points:
                continue

            industries = self.classify_industry(text)

            for industry in industries:
                for pain_point in pain_points:
                    self.pain_points_by_industry[industry].append({
                        "pain_point": pain_point,
                        "source": post['url'],
                        "score": post['score'],
                        "timestamp": datetime.now().isoformat()
                    })

    def deduplicate_pain_points(self) -> None:
        """Remove duplicate pain points within each industry."""
        for industry in self.pain_points_by_industry:
            seen = set()
            unique_points = []

            for point_obj in self.pain_points_by_industry[industry]:
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

        print(f"Results saved to {self.output_file}")

    def print_summary(self) -> None:
        """Print a summary of findings."""
        print("\n" + "="*60)
        print("BUSINESS PAIN POINTS BY INDUSTRY (DEMO DATA)")
        print("="*60)

        for industry in sorted(self.pain_points_by_industry.keys()):
            points = self.pain_points_by_industry[industry]
            print(f"\n{industry} ({len(points)} pain points)")
            print("-" * 40)

            for i, point_obj in enumerate(points[:5], 1):
                pain_point = point_obj["pain_point"][:100]
                print(f"{i}. {pain_point}")
                print(f"   Score: {point_obj['score']}")

def main():
    """Main entry point."""
    scraper = DemoPainPointsScraper()

    print("Running Demo Business Pain Points Scraper...")
    print("Using sample data (no Reddit API required)\n")

    scraper.process_sample_data()
    scraper.deduplicate_pain_points()
    scraper.save_results()
    scraper.print_summary()

if __name__ == "__main__":
    main()
