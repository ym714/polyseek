# How Does Polyseek Sentient Agent Work?

## 🏗️ Architecture Overview

Polyseek Sentient Agent uses a **modular, parallel-processing architecture** that aggregates data from multiple sources and synthesizes it using LLM-based reasoning.

```
┌─────────────────────────────────────────────────────────────┐
│              Polyseek Sentient Agent                        │
│         (Sentient Agent Framework Integration)             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Input: Market URL                                          │
│    ↓                                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Phase 1: Parallel Data Collection                 │   │
│  │  ┌──────────────┬──────────────┬─────────────────┐ │   │
│  │  │ fetch_market │ scrape_      │ signals_client  │ │   │
│  │  │              │ context      │                 │ │   │
│  │  │ • API calls  │ • HTML parse │ • News API      │ │   │
│  │  │ • Metadata   │ • Comments   │ • X/Twitter     │ │   │
│  │  │ • Prices     │ • Rules      │ • RSS feeds     │ │   │
│  │  └──────────────┴──────────────┴─────────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│    ↓                                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Phase 2: LLM-Based Analysis                        │   │
│  │  ┌──────────────────────────────────────────────┐   │   │
│  │  │  Quick Mode: Single-Pass Analysis          │   │   │
│  │  │  OR                                         │   │   │
│  │  │  Deep Mode: 4-Step Analysis                │   │   │
│  │  │   1. Planner → 2. Critic →                │   │   │
│  │  │   3. Follow-up → 4. Final                  │   │   │
│  │  └──────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
│    ↓                                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Phase 3: Report Formatting                        │   │
│  │  • JSON validation                                 │   │
│  │  • Markdown generation                             │   │
│  │  • Source deduplication                            │   │
│  └─────────────────────────────────────────────────────┘   │
│    ↓                                                         │
│  Output: Structured JSON + Markdown Report                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Step-by-Step Data Flow

### **Step 1: Input Parsing** (`main.py`)
- Receives market URL from user (via Sentient Chat or CLI)
- Parses optional parameters:
  - `depth`: `"quick"` (30s) or `"deep"` (120s)
  - `perspective`: `"neutral"` or `"devils_advocate"`
- Emits `RECEIVED` event to show analysis has started

### **Step 2: Parallel Data Collection** (Async, ~5-15 seconds)

Three independent tasks run **simultaneously** to maximize speed:

#### **2a. Market Data Fetching** (`fetch_market.py`)
- **Detects platform**: Polymarket or Kalshi from URL
- **Calls official API**:
  - Polymarket: `https://gamma-api.polymarket.com`
  - Kalshi: `https://trading-api.kalshi.com` (requires auth)
- **Extracts**:
  - Market title, category, deadline
  - Current prices (YES/NO odds)
  - Liquidity and 24h volume
  - Resolution rules
  - Market ID and type
- **Returns**: `MarketData` object

#### **2b. Context Scraping** (`scrape_context.py`)
- **Fetches HTML** of market page using `httpx`
- **Parses with BeautifulSoup**:
  - Extracts resolution rules (from `<div class="rules">` or similar)
  - Scrapes recent comments (configurable count: 5-20)
  - Filters spam/toxic content
- **Analyzes comments**:
  - Basic sentiment analysis (pro/con/neutral)
  - Language detection
  - Character limit enforcement (500 chars per comment)
- **Returns**: `MarketContext` object with rules and comments

#### **2c. External Signals Collection** (`signals_client.py`)
- **Builds search queries** from market title + keywords
- **Calls multiple providers** (pluggable architecture):
  - **News API**: Searches for relevant news articles
  - **X/Twitter API**: Searches for tweets (if token provided)
  - **RSS Feeds**: Fallback to RSS aggregators
- **Processes results**:
  - Extracts title, URL, snippet
  - Assigns sentiment (pro/con/neutral)
  - Adds credibility score and engagement metrics
  - Records timestamp and language
- **Applies rate limiting** and exponential backoff for API calls
- **Returns**: List of `SignalRecord` objects (max 10 per source)

### **Step 3: Data Aggregation** (`main.py`)
- **Merges** all three data sources into unified `AnalysisRequest`
- **Emits progress events**:
  - `MARKET_METADATA`: Shows market title, deadline, prices
  - `DEEP_MODE`: If deep mode is enabled
- **Validates** data completeness

### **Step 4: LLM-Based Analysis** (`analysis_agent.py`)

The core intelligence layer. Two modes available:

#### **Quick Mode** (~30 seconds, single-pass)
1. **Builds comprehensive prompt** containing:
   - Market metadata (title, prices, deadline, rules)
   - Comment summary (top comments with sentiment)
   - External signals (news, social media)
   - Mode flags (depth, perspective)
2. **Sends to LLM** with structured JSON output format
3. **Receives analysis** with:
   - Verdict (YES/NO/UNCERTAIN)
   - Confidence percentage (0-100)
   - Key drivers (top 3 factors with source citations)
   - Uncertainty factors
   - Sources list

#### **Deep Mode** (~120 seconds, 4-step process)

**Step 4a. Planner** (~20s)
- LLM creates an **analysis plan**:
  - Key questions to answer
  - Information gaps to fill
  - Analysis methodology
- Output: Structured plan JSON

**Step 4b. Critic** (~20s)
- LLM **critically evaluates** the plan:
  - Identifies gaps and biases
  - Suggests missing information
  - Recommends follow-up queries
- Output: Critique with gaps and recommendations

**Step 4c. Follow-up** (~30s)
- Uses critique to **gather additional data** (if needed)
- May trigger additional signal searches
- Merges new data with original dataset

**Step 4d. Final Analysis** (~50s)
- **Comprehensive synthesis**:
  - Considers original plan
  - Incorporates critique findings
  - Evaluates all evidence (original + follow-up)
  - Applies Bayesian-style reasoning
  - Produces final verdict with higher confidence

**Bias Mitigation Features:**
- **Devil's Advocate mode**: Forces analysis to find at least 2 counter-arguments
- **Uncertainty factors**: Explicitly lists unknowns and risks
- **Source citations**: All claims must reference specific sources
- **Confidence calibration**: Lower confidence when evidence is insufficient

### **Step 5: Report Formatting** (`report_formatter.py`)
- **Validates JSON schema** against `AnalysisModel` (Pydantic)
- **Enforces limits**:
  - Max 3 key drivers
  - Max 10 sources
  - Required fields present
- **Deduplicates** sources by URL
- **Generates Markdown** report with sections:
  - Verdict & Confidence
  - Summary
  - Key Drivers (with source citations)
  - Risks / Uncertainty Factors
  - Next Steps (if provided)
  - Sources (categorized by type: market/comment/sns/news)
- **Adds metadata**:
  - Analysis timestamp
  - Mode and perspective used
  - Market snapshot (odds, ID, type)

### **Step 6: Output Streaming** (`main.py`)
- **Emits structured JSON**: `ANALYSIS_JSON` event
- **Streams Markdown**: `ANALYSIS_MARKDOWN` event (chunked)
- **Completes**: `COMPLETE` event

## 🎯 Key Design Decisions

### **1. Parallel Processing**
- Three data collection tasks run **simultaneously** (not sequentially)
- Reduces total time from ~45s to ~15s for data collection
- Uses Python `asyncio` for efficient concurrency

### **2. Pluggable Signal Providers**
- Modular architecture allows easy addition of new data sources
- Each provider implements `SignalProvider` protocol
- Fallback mechanisms (RSS if APIs fail)

### **3. Structured Output**
- **JSON** for programmatic use (APIs, integrations)
- **Markdown** for human readability (display in chat)
- Both formats contain identical information

### **4. Mode Flexibility**
- **Quick mode**: Fast analysis for rapid decisions
- **Deep mode**: Comprehensive analysis with multi-step reasoning
- User chooses based on needs (speed vs. depth)

### **5. Bias Mitigation**
- **Devil's Advocate**: Forces counter-argument consideration
- **Uncertainty factors**: Explicitly states unknowns
- **Source citations**: All claims must be backed by sources
- **Confidence calibration**: Lower confidence when evidence is weak

## 📊 Performance Characteristics

| Metric | Quick Mode | Deep Mode |
|--------|------------|-----------|
| **Total Time** | ~30 seconds | ~120 seconds |
| **Data Collection** | ~10 seconds | ~15 seconds |
| **LLM Analysis** | ~20 seconds | ~105 seconds |
| **Report Formatting** | <1 second | <1 second |
| **Sources Analyzed** | 5-15 | 15-30 |
| **Comments Scraped** | 5 | 20 |
| **Analysis Steps** | 1 | 4 |

## 🔧 Technical Stack

- **Language**: Python 3.8+
- **Async Framework**: `asyncio` for concurrent operations
- **HTTP Client**: `httpx` for API calls and web scraping
- **HTML Parsing**: `BeautifulSoup4` for comment extraction
- **LLM Integration**: `litellm` (supports OpenAI, Anthropic, Google, OpenRouter)
- **Data Validation**: `pydantic` for schema validation
- **Framework**: `sentient-agent-framework` for Sentient Chat integration

## 🎨 Example Flow

**Input:**
```json
{
  "market_url": "https://polymarket.com/event/trump-approval-rating-2025",
  "depth": "quick",
  "perspective": "neutral"
}
```

**Process:**
1. ✅ Fetch market data (5s) → Get prices, rules, metadata
2. ✅ Scrape comments (8s) → Extract top 5 comments
3. ✅ Gather signals (10s) → Fetch 10 news articles
4. ✅ LLM analysis (20s) → Single-pass reasoning
5. ✅ Format report (<1s) → Generate JSON + Markdown

**Output:**
- **JSON**: Structured analysis with verdict, confidence, drivers, sources
- **Markdown**: Human-readable report with same information

**Total Time**: ~30 seconds (vs. 30+ minutes manual analysis)

---

**In summary**: Polyseek Sentient Agent solves the problem by **automating data collection**, **systematizing analysis**, and **producing structured, evidence-based reports** in seconds rather than hours.

