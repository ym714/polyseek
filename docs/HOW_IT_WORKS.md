# How It Works

## Architecture

3-phase parallel architecture:

1. **Parallel Data Collection** (~10-15s)
   - Market API calls (Polymarket/Kalshi)
   - HTML scraping (comments, rules)
   - External signals (News API, X/Twitter, RSS)

2. **LLM-Based Analysis** (~20s Quick / ~105s Deep)
   - Quick: Single-pass reasoning
   - Deep: 4-step (Planner → Critic → Follow-up → Final)

3. **Report Formatting** (<1s)
   - JSON validation
   - Markdown generation
   - Source deduplication

## Key Features

- **Parallel processing**: 3x faster than sequential
- **Bias mitigation**: Devil's Advocate mode, uncertainty factors
- **Structured output**: JSON + Markdown
- **Flexible modes**: Quick (speed) or Deep (comprehensive)

## Performance

- Quick mode: ~30 seconds
- Deep mode: ~120 seconds
- Sources analyzed: 5-30 per analysis
