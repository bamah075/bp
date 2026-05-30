# Business Pain Points by Industry

A tool to scrape Reddit for business-related pain points and automatically classify them by industry. This project includes both a real Reddit scraper (requiring API credentials) and a demo version with sample data.

## Features

- **Reddit Scraper**: Scrapes multiple business-focused subreddits (business, entrepreneur, startup, smallbusiness, bizapps)
- **Industry Classification**: Automatically categorizes pain points into 10 industries:
  - Healthcare
  - Finance
  - Technology
  - Retail
  - Manufacturing
  - Real Estate
  - HR & Recruitment
  - Marketing
  - Education
  - Hospitality

- **Pain Point Extraction**: Intelligently identifies pain point statements from Reddit posts
- **Web Dashboard**: Beautiful interactive dashboard to view and export results
- **CSV Export**: Export findings for further analysis

## Quick Start (Demo Mode)

### 1. Run the Demo Scraper
```bash
python3 demo_scraper.py
```

This generates `pain_points_by_industry.json` with sample data (no API keys needed).

### 2. View Results
Open `index.html` in a web browser or serve it:
```bash
# Using Python 3
python3 -m http.server 8000

# Then visit: http://localhost:8000
```

## Using the Real Reddit Scraper

### 1. Get Reddit API Credentials
- Go to: https://www.reddit.com/prefs/apps
- Create a new application ("script" type)
- Note your `client_id` and `client_secret`

### 2. Set Environment Variables
```bash
export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USER_AGENT="pain-points-scraper/1.0"
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Scraper
```bash
python3 reddit_scraper.py
```

This generates `pain_points_by_industry.json` with real Reddit data.

### 5. View Results
```bash
python3 -m http.server 8000
# Visit: http://localhost:8000
```

## Project Structure

```
bp/
├── reddit_scraper.py          # Real Reddit scraper (requires API credentials)
├── demo_scraper.py            # Demo version with sample data
├── index.html                 # Web dashboard
├── requirements.txt           # Python dependencies
├── pain_points_by_industry.json # Generated output (created after running scrapers)
└── README.md                  # This file
```

## How It Works

### 1. Data Collection
The scrapers fetch posts from business-related subreddits using specific search terms.

### 2. Pain Point Extraction
Natural language patterns identify statements containing:
- "problem" / "problems"
- "challenge" / "challenges"
- "struggle" / "struggles"
- "difficult"
- "issue" / "issues"
- "pain"
- "frustrated"
- "nightmare"

### 3. Industry Classification
Each pain point is classified using keyword matching across 10 industries. A single pain point can belong to multiple industries.

### 4. Deduplication
Duplicate pain points are removed while preserving metadata (score, source, timestamp).

### 5. Output
Results are saved as JSON and can be viewed in the web dashboard or exported as CSV.

## Output Format

```json
{
  "generated_at": "2024-05-30T12:34:56.789012",
  "total_industries": 8,
  "total_pain_points": 45,
  "industries": {
    "Healthcare": {
      "count": 5,
      "pain_points": [
        {
          "pain_point": "Problem with EHR integration",
          "source": "https://reddit.com/...",
          "score": 245,
          "timestamp": "2024-05-30T12:00:00"
        },
        ...
      ]
    },
    ...
  }
}
```

## Customization

### Add More Industries
Edit `INDUSTRY_KEYWORDS` in the scraper files to add new industries or modify existing ones.

### Change Subreddits
Modify the `SUBREDDITS` list to scrape different communities:
```python
SUBREDDITS = [
    "business",
    "entrepreneur",
    "startup",
    # Add more here
]
```

### Adjust Scrape Limit
Change the `limit_per_subreddit` parameter when calling `scrape_all()`:
```python
scraper.scrape_all(limit_per_subreddit=100)  # Scrape more posts
```

## Limitations

- Reddit API rate limits apply to the real scraper
- Classification is keyword-based, not ML-based (simpler but less accurate)
- Requires subreddit posts to be in English
- Pain point extraction uses regex patterns (heuristic-based)

## Future Improvements

- Add sentiment analysis to prioritize severe pain points
- Use machine learning for industry classification
- Support multiple languages
- Add trend analysis (track pain points over time)
- Create REST API for programmatic access
- Add filtering and search functionality
- Expand to other platforms (Hacker News, Twitter, etc.)

## License

MIT License - feel free to use and modify!
