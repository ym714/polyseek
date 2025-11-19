# Polyseek 使用ガイド

## ✅ 現在の状態

**Polyseekは使用可能です！**

### 設定済みの機能
- ✅ LLM APIキー: 設定済み（OpenRouter経由）
- ✅ News API: 設定済み
- ✅ Polymarket API: 公開API（認証不要）
- ⚠️ Kalshi API: 未設定（必要に応じて設定可能）
- ⚠️ X/Reddit API: 未設定（オプション）

## 🚀 使い方

### 基本的な使い方

```bash
cd /Users/motoki/projects/polyseek_sentient
export PYTHONPATH="src:$PYTHONPATH"

python3 -c "
import sys
sys.path.insert(0, 'src')
from polyseek_sentient.main import _run_cli
import asyncio

# 実際のPolymarketマーケットURLを指定
url = 'https://polymarket.com/event/your-market-slug'
asyncio.run(_run_cli(url, 'quick', 'neutral'))
"
```

### 実行スクリプトを使う

```bash
cd /Users/motoki/projects/polyseek_sentient

# オフラインモード（テスト用）
./run_polyseek.sh --offline "https://polymarket.com/event/test"

# 実際のマーケット分析
./run_polyseek.sh "https://polymarket.com/event/actual-market-slug"
```

### モードとオプション

- **depth**: `quick` (約30秒) または `deep` (約120秒)
- **perspective**: `neutral` または `devils_advocate`

例：
```bash
# Deepモード + Devil's Advocate視点
asyncio.run(_run_cli(url, 'deep', 'devils_advocate'))
```

## 📊 出力例

実行すると以下のような出力が得られます：

### JSON出力
```json
{
  "verdict": "YES|NO|UNCERTAIN",
  "confidence_pct": 0-100,
  "summary": "...",
  "key_drivers": [
    {
      "text": "...",
      "source_ids": ["SRC1", "SRC2"]
    }
  ],
  "uncertainty_factors": ["..."],
  "sources": [
    {
      "id": "SRC1",
      "title": "...",
      "url": "...",
      "type": "market|comment|sns|news",
      "sentiment": "pro|con|neutral"
    }
  ]
}
```

### Markdown出力
```
### Verdict: **YES**
- Confidence: **75.5%**
- Generated at: 2025-11-19T18:00:41

#### Summary
...

#### Key Drivers
- Driver 1 _(sources: SRC1, SRC2)_
- Driver 2 _(sources: SRC3)_

#### Risks / Uncertainty
- Risk 1
- Risk 2

#### Sources
- **MARKET**
  - [Market Title](url) (neutral)
- **NEWS**
  - [News Title](url) (pro)
```

## 🔧 Sentient Agent Frameworkとの統合

```python
from polyseek_sentient import PolyseekSentientAgent
from sentient_agent_framework import Session, Query, ResponseHandler

agent = PolyseekSentientAgent()

# Sentient Chatで使用
async def analyze_market(market_url: str):
    session = Session(id="user-session")
    query = Query(prompt=json.dumps({
        "market_url": market_url,
        "depth": "quick",
        "perspective": "neutral"
    }))
    
    class MyHandler(ResponseHandler):
        async def emit_json(self, event_name, data):
            print(f"[{event_name}]", data)
        # ... 他のメソッド
    
    await agent.assist(session, query, MyHandler())
```

## ⚙️ 環境変数

必要に応じて設定：

```bash
# LLM APIキー（必須）
export POLYSEEK_LLM_API_KEY="your-key"
# または
export OPENROUTER_API_KEY="your-key"
# または
export OPENAI_API_KEY="your-key"

# News API（オプション、既に設定済み）
export NEWS_API_KEY="your-key"

# Kalshi API（Kalshiマーケット分析用、オプション）
export KALSHI_API_KEY="your-key"
export KALSHI_API_SECRET="your-secret"

# X/Twitter API（オプション）
export X_BEARER_TOKEN="your-token"

# Reddit API（オプション）
export REDDIT_CLIENT_ID="your-id"
export REDDIT_CLIENT_SECRET="your-secret"

# オフラインモード（テスト用）
export POLYSEEK_OFFLINE=1
```

## 🐛 トラブルシューティング

### マーケットが見つからない
```
MarketFetchError: No market found for slug 'xxx'
```
→ URLが正しいか確認してください。Polymarketの実際のマーケットURLを使用してください。

### LLM APIエラー
```
LLM API call failed
```
→ APIキーが正しく設定されているか確認してください。

### タイムアウト
→ `deep`モードは時間がかかります（約120秒）。`quick`モード（約30秒）を試してください。

## 📝 注意事項

1. **Polymarket API**: 公開APIなので認証不要ですが、レート制限があります
2. **Kalshi**: 認証が必要です（設定していない場合は使用できません）
3. **外部シグナル**: News APIは設定済みですが、X/Redditは未設定です
4. **オフラインモード**: テスト用に`POLYSEEK_OFFLINE=1`を設定すると、スタブデータを使用します

## 🎯 次のステップ

実際のマーケットURLを指定して実行してみてください：

```bash
# 例：実際のPolymarketマーケットURL
python3 -c "
import sys
sys.path.insert(0, 'src')
from polyseek_sentient.main import _run_cli
import asyncio
asyncio.run(_run_cli('https://polymarket.com/event/your-actual-market-slug', 'quick', 'neutral'))
"
```

