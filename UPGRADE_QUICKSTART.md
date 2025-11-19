# Polyseek クイックアップグレードガイド

## 🚀 すぐに始められるアップグレード

### 1. X/Twitter統合を追加

```bash
# 依存関係を追加
pip install tweepy python-dotenv

# 環境変数を設定
export X_BEARER_TOKEN="your-twitter-bearer-token"
```

### 2. Reddit統合を追加

```bash
# 依存関係を追加
pip install praw

# 環境変数を設定
export REDDIT_CLIENT_ID="your-reddit-client-id"
export REDDIT_CLIENT_SECRET="your-reddit-client-secret"
export REDDIT_USER_AGENT="polyseek/1.0"
```

### 3. コメント分析の強化

```bash
# 依存関係を追加
pip install langdetect deep-translator
```

### 4. キャッシュ機能の追加

```bash
# 依存関係を追加
pip install cachetools
# またはRedisを使用する場合
pip install redis
```

## 📝 実装手順

### Step 1: Twitter統合の実装

`src/polyseek_sentient/signals_client.py`に以下を追加:

```python
class TwitterSignalProvider:
    def __init__(self, bearer_token: Optional[str], max_results: int = 10):
        self.bearer_token = bearer_token
        self.max_results = max_results
    
    @property
    def available(self) -> bool:
        return bool(self.bearer_token)
    
    async def search(self, query: str) -> List[SignalRecord]:
        if not self.available:
            return []
        # Twitter API v2実装
        # ...
```

### Step 2: Reddit統合の実装

`src/polyseek_sentient/signals_client.py`に以下を追加:

```python
class RedditSignalProvider:
    def __init__(self, client_id: Optional[str], client_secret: Optional[str], 
                 user_agent: Optional[str], max_results: int = 10):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.max_results = max_results
    
    @property
    def available(self) -> bool:
        return bool(self.client_id and self.client_secret)
    
    async def search(self, query: str) -> List[SignalRecord]:
        if not self.available:
            return []
        # Reddit API実装
        # ...
```

### Step 3: gather_signals関数を更新

```python
async def gather_signals(...):
    # 既存のコード...
    
    # Twitterプロバイダーを追加
    twitter_provider = TwitterSignalProvider(settings.apis.x_bearer_token)
    if twitter_provider.available:
        providers.append(twitter_provider)
    
    # Redditプロバイダーを追加
    reddit_provider = RedditSignalProvider(
        settings.apis.reddit_client_id,
        settings.apis.reddit_client_secret,
        os.getenv('REDDIT_USER_AGENT', 'polyseek/1.0')
    )
    if reddit_provider.available:
        providers.append(reddit_provider)
```

## 🎯 次のステップ

1. **X/Twitter統合**から始める（最も影響が大きい）
2. **Reddit統合**を追加
3. **コメント分析の強化**を実装
4. **キャッシュ機能**を追加してパフォーマンスを改善

詳細は `UPGRADE_PLAN.md` を参照してください。

