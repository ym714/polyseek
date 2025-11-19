# Polyseek Sentient Agent (MVP)

This package contains a Sentient-compatible agent that analyzes Polymarket/Kalshi markets without Valyu.  
It fetches market metadata, scrapes on-page context, pulls external signals (news, X, Reddit via pluggable providers), runs an LLM-based synthesis, and returns a Markdown + JSON verdict.

## Key Features
- URL-based market detection (Polymarket/Kalshi)
- Resolution rules + comment scraping with BeautifulSoup
- Pluggable signal providers (News API example included)
- Prompt-engineered LLM analysis with Bayesian-style reasoning
- Markdown + JSON output via a strict schema

## Project Layout
```
src/polyseek_sentient/
  main.py               # Sentient agent entry point
  config.py             # settings + env loading
  fetch_market.py       # official API integration helpers
  scrape_context.py     # comment/rules extraction utilities
  signals_client.py     # external signal aggregation
  analysis_agent.py     # LLM orchestration
  report_formatter.py   # schema validation + Markdown builder
  tests/test_report_formatter.py
```

## Quickstart
1. Install deps: `pip install -r requirements.txt`
2. Export API keys (see `config.py` for names). At minimum you need one LLM key (OpenRouter/OpenAI via LiteLLM). Polymarket access is public, Kalshi requires credentials. Set `POLYSEEK_OFFLINE=1` to use stubbed data without network access.
3. Run the demo CLI:
   ```bash
   python -m polyseek_sentient.main "https://polymarket.com/event/..."
   ```
4. When embedding inside Sentient Agent Framework, instantiate `PolyseekSentientAgent` and wire it into your server/orchestrator.

## Tests
```
pytest src/polyseek_sentient/tests/test_report_formatter.py
```

The test only covers the formatter; extend as you plug real signal providers.
