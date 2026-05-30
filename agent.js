const Anthropic = require('@anthropic-ai/sdk');
require('dotenv').config();

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

// Multi-agent orchestrator for Substack content analysis
class SubstackAgentOrchestrator {
  constructor() {
    this.fetcher = null;
    this.analyzer = null;
    this.summarizer = null;
  }

  async runFetcherAgent(query) {
    console.log(`[FETCHER] Searching Substack for: ${query}`);

    const response = await client.messages.create({
      model: 'claude-opus-4-8',
      max_tokens: 1024,
      messages: [
        {
          role: 'user',
          content: `You are a Substack content fetcher. Generate a JSON array of article metadata for Substack posts about: "${query}".

Include fields: title, publication, summary, url, category, date.
Focus on AI agents, skills, and multi-agent systems.
Return ONLY valid JSON array, no markdown formatting.`
        }
      ]
    });

    try {
      const content = response.content[0].text;
      return JSON.parse(content);
    } catch (e) {
      console.error('Parse error in fetcher agent');
      return [];
    }
  }

  async runAnalyzerAgent(articles) {
    console.log(`[ANALYZER] Analyzing ${articles.length} articles`);

    const response = await client.messages.create({
      model: 'claude-opus-4-8',
      max_tokens: 2048,
      messages: [
        {
          role: 'user',
          content: `You are an AI agent content analyst. Analyze these articles and extract key insights:

${JSON.stringify(articles, null, 2)}

For each article, identify:
1. Key technical concepts
2. Practical applications
3. Relevance to multi-agent systems
4. Innovation level (1-5)

Return a JSON object with analyzed insights for each article.`
        }
      ]
    });

    try {
      const content = response.content[0].text;
      return JSON.parse(content);
    } catch (e) {
      console.error('Parse error in analyzer agent');
      return {};
    }
  }

  async runSummarizerAgent(articles, analysis) {
    console.log(`[SUMMARIZER] Creating daily summary`);

    const response = await client.messages.create({
      model: 'claude-opus-4-8',
      max_tokens: 2048,
      messages: [
        {
          role: 'user',
          content: `You are a summary agent. Create a concise daily digest of AI agent content.

Articles:
${JSON.stringify(articles, null, 2)}

Analysis:
${JSON.stringify(analysis, null, 2)}

Generate a JSON object with:
1. topInsights: array of 3-5 key insights across all articles
2. trendingTopics: array of trending topics
3. recommendedReading: top 3 articles with reasoning
4. dailyTip: one practical tip for using AI agents

Return ONLY valid JSON.`
        }
      ]
    });

    try {
      const content = response.content[0].text;
      return JSON.parse(content);
    } catch (e) {
      console.error('Parse error in summarizer agent');
      return {
        topInsights: [],
        trendingTopics: [],
        recommendedReading: [],
        dailyTip: ''
      };
    }
  }

  async orchestrate() {
    console.log('\n=== SUBSTACK AI AGENT DASHBOARD ===');
    console.log(`Starting multi-agent orchestration at ${new Date().toISOString()}\n`);

    try {
      // Stage 1: Fetcher Agent finds content
      const queries = [
        'AI agents skills Substack',
        'multi-agent orchestration dashboard',
        'autonomous agent patterns'
      ];

      let allArticles = [];
      for (const query of queries) {
        const articles = await this.runFetcherAgent(query);
        allArticles = allArticles.concat(articles);
      }

      console.log(`\n[ORCHESTRATOR] Fetched ${allArticles.length} articles\n`);

      // Stage 2: Analyzer Agent processes content
      const analysis = await this.runAnalyzerAgent(allArticles);
      console.log(`[ORCHESTRATOR] Analysis complete\n`);

      // Stage 3: Summarizer Agent creates digest
      const summary = await this.runSummarizerAgent(allArticles, analysis);
      console.log(`[ORCHESTRATOR] Summary created\n`);

      // Combine results
      const dailySummary = {
        date: new Date().toISOString().split('T')[0],
        timestamp: new Date().toISOString(),
        articles: allArticles,
        analysis: analysis,
        digest: summary,
        agentMetadata: {
          fetcher: 'Article discovery agent',
          analyzer: 'Content analysis agent',
          summarizer: 'Digest creation agent',
          orchestrator: 'Multi-agent coordinator'
        }
      };

      console.log('=== DAILY SUMMARY COMPLETE ===\n');
      console.log(JSON.stringify(dailySummary, null, 2));

      return dailySummary;
    } catch (error) {
      console.error('Orchestration error:', error.message);
      throw error;
    }
  }
}

// Main execution
async function main() {
  const orchestrator = new SubstackAgentOrchestrator();
  const summary = await orchestrator.orchestrate();
  process.exit(0);
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
