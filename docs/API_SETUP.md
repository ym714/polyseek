# API Setup Guide

## Required

### LLM API (Required)
```bash
export GOOGLE_API_KEY="your-key"
# or OPENROUTER_API_KEY, OPENAI_API_KEY, POLYSEEK_LLM_API_KEY
```

**Get keys**: Google (makersuite.google.com), OpenRouter (openrouter.ai), OpenAI (platform.openai.com)

## Optional

### News API (Recommended)
- Free: 100 requests/day
- Setup: `export NEWS_API_KEY="your-key"`
- Get key: https://newsapi.org/register

### Reddit API (Recommended)
- Free, commercial use allowed
- Setup:
  ```bash
  export REDDIT_CLIENT_ID="your-id"
  export REDDIT_CLIENT_SECRET="your-secret"
  export REDDIT_USER_AGENT="polyseek/1.0"
  ```
- Get credentials: https://www.reddit.com/prefs/apps

### X/Twitter API
- Free plan: Very limited
- Paid: $100-$5000/month
- Setup: `export X_BEARER_TOKEN="your-token"`
- Get key: https://developer.twitter.com

### Kalshi API (For Kalshi markets)
- Setup:
  ```bash
  export KALSHI_API_KEY="your-key"
  export KALSHI_API_SECRET="your-secret"
  ```
- Get credentials: https://trading-api.kalshi.com

## Testing

```bash
# Test with specific API
export NEWS_API_KEY="your-key"
python -m polyseek_sentient.main "https://polymarket.com/event/test" --depth quick
```

## Recommended Setup

**Minimum**: LLM API + News API (free tier)

**Recommended**: LLM API + News API + Reddit API (all free)
