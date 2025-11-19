# Quick Start Guide

## Installation

```bash
pip install -r requirements.txt
pip install sentient-agent-framework
```

## Environment Setup

```bash
# LLM API Key (required)
export GOOGLE_API_KEY="your-key"
# or OPENROUTER_API_KEY, OPENAI_API_KEY, POLYSEEK_LLM_API_KEY

# Optional APIs
export NEWS_API_KEY="your-key"
export REDDIT_CLIENT_ID="your-id"
export REDDIT_CLIENT_SECRET="your-secret"
export X_BEARER_TOKEN="your-token"
```

## Usage

### Scripts (Recommended)

```bash
# Quick mode (~30s)
./scripts/run_simple.sh "https://polymarket.com/event/your-market-slug"

# Deep mode (~120s)
./scripts/run_simple.sh "https://polymarket.com/event/your-market-slug" deep neutral

# Devil's Advocate
./scripts/run_simple.sh "https://polymarket.com/event/your-market-slug" quick devils_advocate
```

### Python CLI

```bash
export PYTHONPATH="src:$PYTHONPATH"
python -m polyseek_sentient.main "https://polymarket.com/event/your-market-slug" --depth quick --perspective neutral
```

### Programmatic

```python
from polyseek_sentient import PolyseekSentientAgent
from sentient_agent_framework import Session, Query, ResponseHandler
import json
import asyncio

agent = PolyseekSentientAgent()

async def analyze_market(market_url: str):
    session = Session(id="user-session")
    query = Query(prompt=json.dumps({
        "market_url": market_url,
        "depth": "quick",  # or "deep"
        "perspective": "neutral"  # or "devils_advocate"
    }))
    
    class MyHandler(ResponseHandler):
        async def emit_json(self, event_name, data):
            print(f"[{event_name}]", json.dumps(data, indent=2))
        async def emit_text_block(self, event_name, content):
            print(f"[{event_name}] {content}")
        def create_text_stream(self, event_name):
            return self
        async def emit_chunk(self, chunk):
            print(chunk, end='')
        async def complete(self):
            print()
    
    await agent.assist(session, query, MyHandler())

asyncio.run(analyze_market("https://polymarket.com/event/your-market-slug"))
```

## Modes

- **Quick**: Single-pass analysis (~30s)
- **Deep**: 4-step analysis (~120s) - see `DEEP_MODE_GUIDE.md`

## Perspectives

- **neutral**: Standard analysis
- **devils_advocate**: Forces counter-argument consideration

## Output

Returns structured JSON + Markdown with verdict, confidence, key drivers, uncertainty factors, and sources.

## Troubleshooting

- **Market not found**: Verify URL is correct
- **LLM API error**: Check API key is set correctly
- **Timeout**: Deep mode takes ~120s, use quick mode for faster results
