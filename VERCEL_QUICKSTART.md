# Vercelデプロイ - クイックスタートガイド

## ✅ 準備完了

変更は既にGitHubにプッシュされています：
- リポジトリ: `https://github.com/ym714/polyseek-sentient-agent.git`
- ブランチ: `main`

## 🚀 デプロイ手順（5分で完了）

### ステップ1: Vercelダッシュボードにアクセス

1. [Vercel Dashboard](https://vercel.com/dashboard) にアクセス
2. アカウントにログイン（GitHubアカウントでログイン推奨）

### ステップ2: プロジェクトをインポート

1. ダッシュボードで **"Add New..."** → **"Project"** をクリック
2. **"Import Git Repository"** を選択
3. GitHubリポジトリ一覧から **`ym714/polyseek-sentient-agent`** を選択
   - 表示されない場合は、**"Configure GitHub App"** で権限を付与してください

### ステップ3: プロジェクト設定

Vercelが自動的に設定を検出します。以下の設定を確認：

- **Framework Preset**: `Other`（自動検出）
- **Root Directory**: `./`（デフォルト）
- **Build Command**: （空欄のまま）
- **Output Directory**: （空欄のまま）
- **Install Command**: （空欄のまま）

**そのまま "Deploy" をクリックしてください。**

### ステップ4: 環境変数の設定

デプロイが完了したら、環境変数を設定します：

1. プロジェクトページで **"Settings"** → **"Environment Variables"** を開く
2. 以下の環境変数を追加：

#### 必須（いずれか1つ以上）

```
GOOGLE_API_KEY=your-google-api-key
```
または
```
OPENAI_API_KEY=your-openai-api-key
```
または
```
OPENROUTER_API_KEY=your-openrouter-api-key
```

#### オプション

```
NEWS_API_KEY=your-news-api-key
REDDIT_CLIENT_ID=your-reddit-client-id
REDDIT_CLIENT_SECRET=your-reddit-client-secret
X_BEARER_TOKEN=your-x-bearer-token
LITELLM_MODEL_ID=gemini/gemini-2.0-flash-001
CORS_ORIGINS=https://your-domain.com
```

3. 各環境変数の **Environment** で以下を選択：
   - ✅ Production
   - ✅ Preview
   - ✅ Development

4. **"Save"** をクリック

### ステップ5: 再デプロイ

環境変数を設定した後、**"Deployments"** タブで最新のデプロイを選択し、**"Redeploy"** をクリックしてください。

## 🎉 完了！

デプロイが完了すると、以下のURLが表示されます：
- **Production URL**: `https://polyseek-sentient-agent-xxxxx.vercel.app`
- **Custom Domain**: （設定した場合）

## 📝 確認事項

デプロイ後、以下を確認してください：

1. **ヘルスチェック**: `https://your-app.vercel.app/api/health` にアクセス
   - `{"status":"ok"}` が返れば成功

2. **フロントエンド**: `https://your-app.vercel.app` にアクセス
   - アプリケーションが表示されれば成功

3. **APIエンドポイント**: フロントエンドから分析機能をテスト

## 🔧 トラブルシューティング

### ビルドエラーが発生した場合

1. **Vercelダッシュボード** → **"Deployments"** → 失敗したデプロイを選択
2. **"Build Logs"** を確認
3. エラーメッセージに基づいて対応：
   - Pythonパスの問題 → `vercel.json` の `PYTHONPATH` を確認
   - 依存関係の問題 → `requirements.txt` を確認

### 環境変数が反映されない場合

1. 環境変数を設定後、**必ず再デプロイ**してください
2. Production環境に設定されているか確認

### APIが動作しない場合

1. **"Logs"** タブでエラーログを確認
2. 環境変数が正しく設定されているか確認
3. `/api/health` エンドポイントで動作確認

## 📚 詳細情報

より詳細な情報は `DEPLOY_VERCEL.md` を参照してください。

## 🔗 リンク

- **GitHubリポジトリ**: https://github.com/ym714/polyseek-sentient-agent
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Vercel Documentation**: https://vercel.com/docs

