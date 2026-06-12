# Australian Business Pain Points Analysis

Analysis and grouping of pain points from the r/ausbusiness subreddit.

## Project Files

### 📊 Analysis Scripts
- **`analyze_pain_points.py`** - Main analysis script that extracts and categorizes pain points
- **`scrape_ausbusiness.py`** - Scraper for fetching data from r/ausbusiness (requires network access)

### 📁 Data Files
- **`sample_data.json`** - Sample dataset with 20 representative posts from r/ausbusiness
- **`pain_points_analysis.json`** - Detailed analysis results with categorized pain points

### 📊 Reports
- **`pain_points_report.html`** - Interactive visualization dashboard (open in browser)

## Pain Points Identified

### 8 Main Categories:

1. **💰 Cash Flow & Finance** (65% of posts)
   - Interest rates, payment delays, loan access challenges
   - Profit margin compression
   - Difficulty accessing affordable financing

2. **💻 Technology & Systems** (30% of posts)
   - Cybersecurity concerns and ransomware threats
   - Digital transformation costs
   - Legacy system modernization challenges
   - SaaS subscription proliferation

3. **⚖️ Compliance & Regulations** (25% of posts)
   - Tax compliance (ABN, GST, PAYG)
   - Workplace relations laws
   - Superannuation obligations
   - Privacy regulations

4. **👥 Staffing & HR** (25% of posts)
   - Difficulty finding skilled workers
   - Staff retention and turnover costs
   - Wage pressure and salary growth
   - Regional skill shortages

5. **📈 Marketing & Sales** (25% of posts)
   - Customer acquisition costs
   - Advertising cost inflation (Google/Facebook)
   - Intense competition
   - Low ROI on marketing spend

6. **🚚 Supply Chain & Operations** (25% of posts)
   - Supplier reliability issues
   - Logistics and freight costs
   - Supply disruption risks
   - Lead time delays

7. **🏢 Real Estate & Facilities** (25% of posts)
   - Rising commercial rents
   - Location challenges
   - Lease renewal cost shocks
   - Regional vs. urban trade-offs

8. **📊 Market & Economic** (20% of posts)
   - Global competition (Amazon, China imports)
   - Economic pressures and inflation
   - Consumer price sensitivity
   - Market saturation

## Key Insights

### 🎯 Top Engagement Issues
The 5 most discussed pain points (by upvotes):
1. Customer payment delays (534 upvotes)
2. Commercial rent affordability (523 upvotes)
3. Access to affordable business loans (445 upvotes)
4. Interest rates impact on cash flow (412 upvotes)
5. Customer acquisition costs (387 upvotes)

### ⚠️ Multi-Category Issues
- Many challenges span multiple categories
- Financial stress intersects with operational, compliance, and staffing challenges
- Location/rent impacts both facilities and staffing challenges

### 📈 Engagement Patterns
- Financial survival issues dominate discussions
- Smaller businesses struggle most with compliance and technology
- Rural/regional businesses face unique staffing challenges

## How to Use

### Run the Analysis
```bash
python3 analyze_pain_points.py
```

### View the Report
Open `pain_points_report.html` in a web browser to see an interactive visualization.

### Modify Analysis
Edit the category keywords in `analyze_pain_points.py` to refine pain point detection.

## Data Source

This analysis is based on:
- **Source**: r/ausbusiness subreddit
- **Posts Analyzed**: 20 representative posts
- **Coverage**: 100% of analyzed posts contain identified pain points
- **Analysis Date**: 2026-06-12

## Technical Notes

- The scraper uses Reddit's JSON API with fallback to sample data
- Pain point detection uses keyword matching across predefined categories
- Results are aggregated by category and post-level details are preserved
- Interactive HTML report provides multiple visualization perspectives
