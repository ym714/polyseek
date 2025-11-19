# Polyseek Sentient 提出ガイド

## 📦 提出用パッケージ構成

Sentient Agent Frameworkに提出する際は、以下の構成で提出することを推奨します：

```
polyseek_sentient/
├── README.md                    # 必須: エージェントの説明とセットアップ手順
├── requirements.txt             # 必須: 依存関係
├── src/
│   └── polyseek_sentient/
│       ├── __init__.py         # PolyseekSentientAgentをエクスポート
│       ├── main.py              # Sentientエージェントのエントリーポイント
│       ├── config.py            # 設定管理
│       ├── fetch_market.py      # マーケットデータ取得
│       ├── scrape_context.py    # コメント・ルール抽出
│       ├── signals_client.py    # 外部シグナル収集
│       ├── analysis_agent.py    # LLM分析
│       ├── report_formatter.py  # レポートフォーマット
│       └── tests/
│           └── test_report_formatter.py
└── .env.example                 # オプション: 環境変数の例
```

## ✅ 提出前に確認すべきこと

### 1. 必須ファイルの確認

- [x] `README.md` - エージェントの説明、セットアップ手順、使用方法
- [x] `requirements.txt` - すべての依存関係が記載されている
- [x] `src/polyseek_sentient/__init__.py` - `PolyseekSentientAgent`がエクスポートされている
- [x] `src/polyseek_sentient/main.py` - `AbstractAgent`を継承した`PolyseekSentientAgent`クラス

### 2. 依存関係の確認

現在の`requirements.txt`:
```
httpx>=0.27.0
beautifulsoup4>=4.12.3
pydantic>=2.8.0
python-dotenv>=1.0.1
litellm>=1.43.6
anyio>=4.4.0
feedparser>=6.0.10
```

**注意**: `sentient-agent-framework`は別途インストールが必要です。

### 3. 環境変数の設定

必要な環境変数:
- `GOOGLE_API_KEY` または `POLYSEEK_LLM_API_KEY` - LLM APIキー
- `NEWS_API_KEY` - News APIキー（オプション）
- `X_BEARER_TOKEN` - X APIトークン（オプション）
- `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET` - Reddit API（オプション）

### 4. 動作確認

提出前に以下を確認:
```bash
# 1. 依存関係のインストール
pip install -r requirements.txt
pip install sentient-agent-framework

# 2. 環境変数の設定
export GOOGLE_API_KEY="your_key"
export NEWS_API_KEY="your_key"

# 3. 動作確認
python -m polyseek_sentient.main "https://polymarket.com/event/..."
```

## 🚀 提出方法

### オプション1: 独立したリポジトリとして提出

1. `polyseek_sentient`ディレクトリを新しいリポジトリにコピー
2. 不要なファイルを削除（`.git`, `__pycache__`, ドキュメントファイルなど）
3. GitHub/GitLabなどにプッシュ
4. SentientにリポジトリURLを提出

### オプション2: Sentient-Agent-Frameworkの`generated_agents`に追加

```bash
# Sentient-Agent-Frameworkリポジトリに追加
cp -r polyseek_sentient /path/to/Sentient-Agent-Framework/generated_agents/
```

### オプション3: PyPIパッケージとして公開（推奨）

1. `setup.py`または`pyproject.toml`を作成
2. PyPIに公開
3. `pip install polyseek-sentient`でインストール可能に

## 📝 提出用README.mdの推奨内容

```markdown
# Polyseek Sentient Agent

Sentient Agent Framework用のPolymarket/Kalshiマーケット分析エージェント。

## 機能

- Polymarket/Kalshiマーケットの自動分析
- 外部シグナル収集（News API, X API, RSS）
- Quick/Deepモード対応
- Devil's Advocate視点サポート

## セットアップ

1. 依存関係のインストール:
   ```bash
   pip install -r requirements.txt
   pip install sentient-agent-framework
   ```

2. 環境変数の設定:
   ```bash
   export GOOGLE_API_KEY="your_key"
   export NEWS_API_KEY="your_key"
   ```

3. 使用方法:
   ```python
   from polyseek_sentient import PolyseekSentientAgent
   # Sentient Agent Frameworkに統合
   ```

## ライセンス

[ライセンス情報]
```

## ⚠️ 注意事項

1. **APIキーの管理**: 環境変数として管理し、リポジトリにコミットしない
2. **依存関係のバージョン**: 互換性を保つため、バージョンを固定することを推奨
3. **テスト**: 基本的なテストが含まれていることを確認
4. **ドキュメント**: READMEに使用方法とセットアップ手順を記載

## 🔍 提出前チェックリスト

- [ ] すべての依存関係が`requirements.txt`に記載されている
- [ ] `README.md`が最新で、セットアップ手順が記載されている
- [ ] 環境変数の例が`.env.example`に記載されている（オプション）
- [ ] テストが実行可能である
- [ ] 不要なファイル（`.pyc`, `__pycache__`, `.git`など）が含まれていない
- [ ] ライセンス情報が明確である
- [ ] `PolyseekSentientAgent`が正しく`AbstractAgent`を継承している
- [ ] `assist`メソッドが正しく実装されている

