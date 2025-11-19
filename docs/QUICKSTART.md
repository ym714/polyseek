# Polyseek クイックスタート

## 基本的な実行コマンド

### 方法1: 実行スクリプトを使用（推奨）

```bash
cd /Users/motoki/projects/polyseek_sentient

# 基本的な実行
./run_analysis.sh "https://polymarket.com/event/your-market-slug"

# オプション指定
./run_analysis.sh "https://polymarket.com/event/your-market-slug" quick neutral
./run_analysis.sh "https://polymarket.com/event/your-market-slug" deep devils_advocate
```

### 方法2: 直接Pythonコマンドで実行

```bash
cd /Users/motoki/projects/polyseek_sentient

export GOOGLE_API_KEY="AIzaSyCRzo5VuNWsV6MBrkz6B0-Pebr-tKIPJS8"
export NEWS_API_KEY="95dd935d45774d9fbfc292e4fe488746"
export LITELLM_MODEL_ID="gemini/gemini-2.0-flash-001"
export PYTHONPATH="src:$PYTHONPATH"

python3 -c "
import sys
sys.path.insert(0, 'src')
from polyseek_sentient.config import Settings, LLMSettings, APISettings
import os
from polyseek_sentient.main import PolyseekSentientAgent
import asyncio
import json

settings = Settings(
    apis=APISettings(news_api_key=os.getenv('NEWS_API_KEY')),
    llm=LLMSettings(
        model=os.getenv('LITELLM_MODEL_ID', 'gemini/gemini-2.0-flash-001'),
        api_key=os.getenv('GOOGLE_API_KEY')
    )
)

class CLIResponseHandler:
    async def emit_text_block(self, event_name, content):
        print(f'[{event_name}] {content}')
    async def emit_json(self, event_name, data):
        import json
        print(f'[{event_name}]', json.dumps(data, indent=2, ensure_ascii=False))
    def create_text_stream(self, event_name):
        return self
    async def emit_chunk(self, chunk):
        print(chunk, end='')
    async def complete(self):
        print()

class SimpleQuery:
    def __init__(self, prompt):
        self.prompt = prompt

class SimpleSession:
    id = 'cli-session'

agent = PolyseekSentientAgent(settings=settings)
query = SimpleQuery(prompt=json.dumps({
    'market_url': 'YOUR_MARKET_URL_HERE',
    'depth': 'quick',
    'perspective': 'neutral'
}))
session = SimpleSession()
handler = CLIResponseHandler()

asyncio.run(agent.assist(session, query, handler))
"
```

### 方法3: 環境変数を設定してから実行

```bash
# 環境変数を設定（.bashrc や .zshrc に追加可能）
export GOOGLE_API_KEY="AIzaSyCRzo5VuNWsV6MBrkz6B0-Pebr-tKIPJS8"
export NEWS_API_KEY="95dd935d45774d9fbfc292e4fe488746"
export LITELLM_MODEL_ID="gemini/gemini-2.0-flash-001"

# 実行
cd /Users/motoki/projects/polyseek_sentient
export PYTHONPATH="src:$PYTHONPATH"
python3 -c "
import sys
sys.path.insert(0, 'src')
from polyseek_sentient.main import _run_cli
import asyncio
asyncio.run(_run_cli('YOUR_MARKET_URL_HERE', 'quick', 'neutral'))
"
```

## 実行例

### NVIDIA決算マーケット
```bash
./run_analysis.sh "https://polymarket.com/event/nvda-quarterly-earnings-nongaap-eps-11-19-2025-1pt25"
```

### Epstein Disclosure Billマーケット
```bash
./run_analysis.sh "https://polymarket.com/event/when-will-trump-sign-the-epstein-disclosure-bill-into-law"
```

## オプション

- **depth**: `quick` (約30秒) または `deep` (約120秒)
- **perspective**: `neutral` または `devils_advocate`

例:
```bash
./run_analysis.sh "URL" deep devils_advocate
```

## 出力

分析結果は以下の形式で出力されます：

1. **MARKET_METADATA**: マーケットの基本情報
2. **ANALYSIS_JSON**: 構造化された分析結果（JSON形式）
3. **ANALYSIS_MARKDOWN**: 読みやすいMarkdown形式のレポート

