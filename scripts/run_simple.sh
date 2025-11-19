#!/bin/bash
# シンプルな実行コマンド

export GOOGLE_API_KEY="AIzaSyCRzo5VuNWsV6MBrkz6B0-Pebr-tKIPJS8"
export NEWS_API_KEY="95dd935d45774d9fbfc292e4fe488746"
export LITELLM_MODEL_ID="gemini/gemini-2.0-flash-001"
export PYTHONPATH="src:$PYTHONPATH"

cd "$(dirname "$0")"

# 引数チェック
if [ $# -eq 0 ]; then
    echo "使用方法: $0 <マーケットURL> [depth] [perspective]"
    echo ""
    echo "例:"
    echo "  $0 'https://polymarket.com/event/your-market-slug'"
    echo "  $0 'https://polymarket.com/event/your-market-slug' quick neutral"
    echo "  $0 'https://polymarket.com/event/your-market-slug' deep devils_advocate"
    exit 1
fi

URL="$1"
DEPTH="${2:-quick}"
PERSPECTIVE="${3:-neutral}"

python3 << PYTHON_SCRIPT
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

url = '$URL'
depth = '$DEPTH'
perspective = '$PERSPECTIVE'

agent = PolyseekSentientAgent(settings=settings)
query = SimpleQuery(prompt=json.dumps({
    'market_url': url,
    'depth': depth,
    'perspective': perspective
}))
session = SimpleSession()
handler = CLIResponseHandler()

asyncio.run(agent.assist(session, query, handler))
PYTHON_SCRIPT
