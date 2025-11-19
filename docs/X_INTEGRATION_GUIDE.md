# X（Twitter）統合ガイド

## 📋 概要

X（旧Twitter）統合により、リアルタイムのソーシャルメディアシグナルを予測市場分析に追加できます。

## 🔑 X APIキーの取得方法

### Step 1: X Developer Portalにアクセス

1. https://developer.twitter.com/ にアクセス
2. Xアカウントでログイン（または新規登録）

### Step 2: 開発者アカウントの申請

1. 「Sign up」をクリック
2. 開発者アカウントの申請フォームに記入
   - 使用目的を説明（例: "予測市場分析のためのデータ収集"）
   - 承認まで数時間〜数日かかる場合があります

### Step 3: プロジェクトとアプリの作成

1. 承認後、Developer Portalにログイン
2. 「Projects & Apps」→「Create Project」をクリック
3. プロジェクト名を入力（例: "Polyseek Analysis"）
4. アプリを作成
5. **Bearer Token**を生成・コピー

### Step 4: APIキーを設定

```bash
export X_BEARER_TOKEN="your-bearer-token-here"
```

または、`.env`ファイルに追加：

```
X_BEARER_TOKEN=your-bearer-token-here
```

## 🚀 使用方法

### 基本的な使用

X APIキーを設定すると、自動的にX検索が有効になります：

```bash
cd /Users/motoki/projects/polyseek_sentient
export X_BEARER_TOKEN="your-bearer-token"
export GOOGLE_API_KEY="your-google-api-key"
export NEWS_API_KEY="your-news-api-key"
export LITELLM_MODEL_ID="gemini/gemini-2.0-flash-001"
export PYTHONPATH="src:$PYTHONPATH"

./run_simple.sh "https://polymarket.com/event/your-market-slug"
```

### 実行例

```bash
./run_simple.sh "https://polymarket.com/event/nvda-quarterly-earnings-nongaap-eps-11-19-2025-1pt25"
```

実行すると、Xからのツイートも分析結果に含まれます：

```json
{
  "sources": [
    {
      "id": "SRC_X1",
      "title": "Tweet by @username",
      "url": "https://twitter.com/username/status/123456",
      "type": "sns",
      "sentiment": "pro",
      "engagement": 150
    }
  ]
}
```

## 📊 X統合の機能

### 取得される情報

- **ツイート本文**: 最大280文字
- **投稿者情報**: ユーザー名、認証済みアカウントかどうか
- **エンゲージメント**: いいね、リツイート、リプライの合計
- **タイムスタンプ**: 投稿日時
- **言語**: ツイートの言語
- **信頼度スコア**: 
  - 認証済みアカウント: +0.2
  - エンゲージメント > 100: +0.2
  - エンゲージメント > 10: +0.1

### 検索クエリの最適化

- マーケットタイトルから主要キーワードを抽出
- 一般的な単語（"Will", "?"など）を除去
- 最大500文字に制限（Twitter APIの制限）

## ⚠️ 注意事項

### API制限

- **レート制限**: Twitter API v2の無料プランでは制限があります
- **月間ツイート数**: プランによって異なります
- **リクエスト頻度**: 15分あたりのリクエスト数に制限があります

### エラーハンドリング

- **401エラー**: Bearer Tokenが無効
- **429エラー**: レート制限超過
- エラー時は自動的にスキップされ、他のシグナルソースは正常に動作します

## 🔧 トラブルシューティング

### Bearer Tokenが認識されない

```bash
# 環境変数を確認
echo $X_BEARER_TOKEN

# スクリプト内で確認
python3 -c "
import os
print('X_BEARER_TOKEN:', os.getenv('X_BEARER_TOKEN', 'NOT SET'))
"
```

### APIエラーが発生する

1. Bearer Tokenが正しいか確認
2. 開発者アカウントが承認されているか確認
3. APIプランの制限を確認
4. レート制限に達していないか確認

### ツイートが取得できない

- 検索クエリが長すぎる可能性があります
- 検索結果が0件の場合もあります（正常な動作）
- エラーログを確認してください

## 📈 次のステップ

X統合が完了したら、以下も検討できます：

1. **Reddit統合**: コミュニティの議論を追加
2. **コメント分析の強化**: 言語判定と翻訳
3. **Deepモード**: より深い分析

詳細は `UPGRADE_PLAN.md` を参照してください。

