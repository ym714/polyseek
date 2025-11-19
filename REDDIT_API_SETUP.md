# Reddit API セットアップガイド

## 🔑 Reddit APIキーの取得手順（詳細版）

### Step 1: Redditアカウントの準備

1. Redditアカウントを持っていない場合、作成してください
   - https://www.reddit.com/register

### Step 2: アプリケーションの作成

1. **Reddit Preferencesにアクセス**
   - https://www.reddit.com/prefs/apps にアクセス
   - または、Redditにログイン後、右上のユーザー名 → **User Settings** → **Privacy & Security** → 下にスクロールして **"apps"** セクションを探す

2. **アプリを作成**
   - ページの一番下にスクロール
   - **"create app"** または **"create another app"** ボタンをクリック

3. **アプリ情報を入力**
   - **name**: アプリ名（例: "Polyseek Analysis"）
   - **app type**: **"script"** を選択（重要！）
   - **description**: 説明（任意、例: "予測市場分析のためのデータ収集"）
   - **about url**: 空白でOK
   - **redirect uri**: `http://localhost:8080` と入力（必須）

4. **作成をクリック**

5. **認証情報を確認**
   - 作成後、アプリの下に表示される：
     - **client_id**: 14文字の文字列（アプリ名の下に表示）
     - **secret**: "secret" という文字列の下に表示される長い文字列

### Step 3: 環境変数の設定

```bash
export REDDIT_CLIENT_ID="your-client-id-here"
export REDDIT_CLIENT_SECRET="your-secret-here"
export REDDIT_USER_AGENT="polyseek/1.0 (by /u/yourusername)"
```

**重要**: `REDDIT_USER_AGENT`は以下の形式にする必要があります：
- `"アプリ名/バージョン (by /u/ユーザー名)"`
- 例: `"polyseek/1.0 (by /u/motoki)"`

## ⚠️ よくある問題と解決方法

### 問題1: "create app"ボタンが見つからない

**解決方法**:
- ページを下にスクロールしてください
- 既存のアプリがある場合、その下にボタンがあります
- ブラウザのキャッシュをクリアして再読み込み

### 問題2: アプリタイプが選択できない

**解決方法**:
- **"script"** を選択してください（他のタイプは認証が複雑）
- ドロップダウンメニューから選択

### 問題3: client_idやsecretが表示されない

**解決方法**:
- アプリを作成後、アプリの下に小さく表示されます
- アプリ名の下に14文字の文字列（client_id）
- "secret"という文字の下に長い文字列（secret）
- 見つからない場合は、アプリを削除して再作成

### 問題4: 認証エラーが発生する

**解決方法**:
- `REDDIT_USER_AGENT`の形式を確認
- ユーザー名が正しいか確認
- client_idとsecretが正しくコピーされているか確認

## 🔄 代替案: Reddit APIなしで使う

Reddit APIが取得できない場合でも、polyseekは動作します：

### 現在利用可能な機能

1. ✅ **News API**: 既に実装済み・動作中
2. ✅ **X API**: 実装済み（無料プランは制限的）
3. ✅ **マーケットデータ**: Polymarket API（公開・無料）
4. ✅ **コメント分析**: スクレイピング（実装済み）

### Redditなしでも十分な理由

- News APIで主要なニュースを取得可能
- マーケットデータとコメントで十分な分析が可能
- Redditは補助的な情報源

## 🧪 テスト方法

Reddit APIを設定したら、以下でテスト：

```bash
cd /Users/motoki/projects/polyseek_sentient
export REDDIT_CLIENT_ID="your-client-id"
export REDDIT_CLIENT_SECRET="your-secret"
export REDDIT_USER_AGENT="polyseek/1.0 (by /u/yourusername)"
export PYTHONPATH="src:$PYTHONPATH"

python3 -c "
import sys
sys.path.insert(0, 'src')
from polyseek_sentient.config import load_settings
settings = load_settings()
print('Reddit Client ID:', settings.apis.reddit_client_id[:10] + '...' if settings.apis.reddit_client_id else 'NOT SET')
print('Reddit Secret:', 'SET' if settings.apis.reddit_client_secret else 'NOT SET')
"
```

## 📝 スクリーンショットガイド（参考）

1. **Reddit Preferencesページ**
   - URL: https://www.reddit.com/prefs/apps
   - ページの一番下に「create app」ボタン

2. **アプリ作成フォーム**
   - name: 任意の名前
   - app type: **"script"** を選択
   - redirect uri: `http://localhost:8080`

3. **認証情報の確認**
   - アプリ作成後、アプリの下に表示される
   - client_id: 14文字の文字列
   - secret: 長い文字列

## 💡 ヒント

- Reddit APIは完全無料で商用利用も可能
- 取得に時間がかかる場合は、News APIのみでも十分動作します
- Reddit統合は後から追加できます

