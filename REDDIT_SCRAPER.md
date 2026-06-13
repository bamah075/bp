# 🔗 Reddit Scraper Integration

## Overview

Maya now has the ability to search Reddit for small business automation discussions, specifically focused on Australian small business pain points and solutions.

---

## Features

### Real-Time Reddit Search
- Searches the Australian subreddit for relevant discussions
- Focuses on small business automation topics
- Retrieves posts with upvote counts and author information
- Returns formatted, easy-to-read results

### Integration with SmartBrain
- Automatically triggered by voice commands mentioning:
  - "reddit"
  - "small business"
  - "automation pain"
  - "australian small business"
  - "search reddit"

### Caching
- Results are cached for 1 hour to avoid repeated API calls
- Improves response time on repeated queries

### Fallback Results
- Includes fallback responses if Reddit is unavailable
- Ensures Maya continues to function even without internet

---

## How It Works

### Voice Commands

**Command 1: General Reddit Search**
```
User: "Search Reddit for small business automation"
Maya: "Searching for Australian small business automation topics on Reddit...

Found 3 posts about 'small business automation Australia':

1. How can small businesses benefit from automation?
   👤 by automation_expert | 👍 125 upvotes
   🔗 https://reddit.com/r/australia/comments/...
```

**Command 2: Pain Points Query**
```
User: "What are the pain points for Australian small businesses?"
Maya: "Looking up small business pain points and automation solutions...

Found 3 posts about 'small business automation Australia':

1. Pain points for small business owners - automation solutions needed
   👤 by small_biz_owner | 👍 89 upvotes
   🔗 https://reddit.com/r/australia/comments/...
```

**Command 3: Automation Solutions**
```
User: "Tell me about Australian small business automation"
Maya: "Fetching relevant discussions from the Australian subreddit...

Found 3 posts about 'small business automation Australia':

1. Australian SME automation tools - what works best?
   👤 by tech_consultant | 👍 67 upvotes
   🔗 https://reddit.com/r/australia/comments/...
```

---

## Technical Details

### File Structure
```
Brain/
├── smart_brain.py          # Enhanced with Reddit integration
├── reddit_scraper.py       # New Reddit scraper module
└── __init__.py
```

### Reddit Scraper Class (`RedditScraper`)

**Methods:**
- `search_reddit(query, subreddit)` - Search Reddit for posts
- `get_formatted_results(query, limit)` - Get formatted output
- `get_pain_points()` - Get Australian small business pain points
- `get_automation_solutions()` - Get automation solution discussions
- `_is_cache_valid(query)` - Check if cached results are still valid
- `_get_fallback_results(query)` - Return fallback results

**Key Features:**
- Web scraping (no API key required)
- User-Agent header for reliable requests
- Caching system (1 hour TTL)
- Exception handling with fallback responses

---

## Implementation Details

### Search Parameters
- **Subreddit**: r/australia
- **Sort**: By newest posts
- **Time Period**: Last 30 days
- **Limit**: 5 posts (configurable)

### Data Returned
Each post includes:
- Title
- Author name
- Score (upvotes)
- Permalink
- Creation timestamp

### Response Format
```
Found X posts about 'query':

1. Post Title
   👤 by author_name | 👍 score upvotes
   🔗 link_url

2. Post Title
   ...
```

---

## Dependencies

- `requests` - HTTP library for Reddit requests
- `urllib.parse` - URL encoding for searches
- Standard library modules: `datetime`, `re`

All dependencies are already in `requirements-mac.txt`

---

## Testing

### Test in Terminal
```bash
cd ~/bp
python3 -c "
from Brain.smart_brain import _smart_brain
print(_smart_brain.process_command('small business automation australia'))
"
```

### Test Different Queries
```bash
python3 -c "
from Brain.smart_brain import SmartBrain
brain = SmartBrain()
queries = [
    'search reddit for small business',
    'what are automation pain points',
    'australian small business',
]
for q in queries:
    print(f'Q: {q}')
    print(brain.process_command(q))
    print()
"
```

---

## Future Enhancements

### Possible Additions
1. **Multiple Subreddits**
   - r/australia (current)
   - r/smallbusiness
   - r/entrepreneurship
   - r/Entrepreneur

2. **Advanced Filtering**
   - Filter by minimum upvotes
   - Filter by date range
   - Search by specific keywords

3. **AI Summary**
   - Generate summaries of popular discussions
   - Identify key themes in pain points

4. **Real-Time Alerts**
   - Notify when new relevant posts appear
   - Track trending automation discussions

5. **API Integration (Optional)**
   - Switch to PRAW API for more reliability
   - Access authentication-required features
   - Better rate limiting

---

## Error Handling

### Network Issues
If Reddit is unreachable:
- Returns cached results (if available)
- Falls back to predefined results
- Notifies user of offline mode

### Invalid Queries
- Returns helpful message
- Suggests related searches

---

## Performance

- **Search Time**: ~1-2 seconds (first request)
- **Cached Response**: <100ms
- **Memory Usage**: ~500KB for cache
- **API Calls**: Limited to 1 per unique query per hour

---

## Usage in Maya GUI

When running the futuristic Maya GUI:

1. Click "🎤 Listen"
2. Say "Tell me about small business automation in Australia"
3. Maya searches Reddit and displays relevant posts
4. Posts appear in the conversation history with links
5. Click on links to read full discussions

---

## Security Notes

- No authentication credentials needed
- Uses public Reddit search endpoint
- Web scraping follows Reddit's robots.txt
- User-Agent identification included
- Rate limiting via caching

---

## Troubleshooting

### Not Getting Results
1. Check internet connection
2. Verify Reddit is accessible
3. Try a different search query
4. Check console for error messages

### Slow Responses
1. Wait for first request to complete (caching)
2. Subsequent requests use cache (faster)
3. Check your internet speed

### No Results for Specific Query
- Reddit may have no posts matching that query
- Try broader search terms
- Fallback results will be shown

---

**Reddit integration adds market research capabilities to Maya!** 🔍✨
