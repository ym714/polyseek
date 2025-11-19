# Deepモード実装ガイド

## ✅ Deepモード実装完了

Deepモードが正常に実装され、動作しています！

## 🔄 Deepモードの4ステップ分析プロセス

### Step 1: Planner（計画フェーズ）
- 分析計画を立てる
- 主要な質問を特定
- 情報のギャップを特定

### Step 2: Critic（批判フェーズ）
- 計画を批判的に検証
- 分析のギャップを特定
- 追加調査が必要な領域を特定
- 潜在的なバイアスを指摘

### Step 3: Follow-up（追加調査フェーズ）
- Criticで特定されたギャップを埋める
- 必要に応じて追加のシグナルを収集
- より深い調査を実施

### Step 4: Final（最終分析フェーズ）
- すべてのデータを統合
- 包括的な分析を実行
- 最終的な判定と信頼度を算出

## 🚀 使用方法

### Deepモードで実行

```bash
cd /Users/motoki/projects/polyseek_sentient
./run_simple.sh "https://polymarket.com/event/your-market-slug" deep neutral
```

### Devil's Advocateモードと組み合わせ

```bash
./run_simple.sh "https://polymarket.com/event/your-market-slug" deep devils_advocate
```

## 📊 Deepモードの特徴

### Quickモードとの比較

| 特徴 | Quickモード | Deepモード |
|------|------------|-----------|
| **分析ステップ** | 1パス | 4ステップ |
| **処理時間** | 約30秒 | 約120秒 |
| **トークン数** | 1,024 | 2,048 |
| **分析の深さ** | 基本的 | 包括的 |
| **反証の検証** | 基本的 | 徹底的 |

### Deepモードのメリット

1. **より深い分析**
   - 計画→批判→追加調査→最終分析の4ステップ
   - より包括的な証拠の評価

2. **ギャップの特定**
   - Criticフェーズで情報の不足を特定
   - 追加調査でギャップを埋める

3. **バイアスの検出**
   - 潜在的なバイアスを指摘
   - より客観的な分析

4. **メタデータの記録**
   - 分析計画を記録
   - 批判の内容を記録
   - 透明性の向上

## 📝 出力例

Deepモードの出力には、以下のメタデータが含まれます：

```json
{
  "verdict": "YES",
  "confidence_pct": 75.0,
  "summary": "...",
  "key_drivers": [...],
  "uncertainty_factors": [...],
  "sources": [...],
  "metadata": {
    "mode": "deep",
    "plan": [
      "Step 1: Analyze market fundamentals",
      "Step 2: Evaluate external evidence",
      ...
    ],
    "critique": {
      "gaps": [
        "Gap 1: Missing information about X",
        ...
      ],
      "follow_up_queries": [
        "Additional search query 1",
        ...
      ]
    }
  }
}
```

## ⚙️ 設定

Deepモードは自動的に有効になります。`depth="deep"`を指定するだけです。

環境変数で調整可能：
- `LLM_MAX_TOKENS`: Deepモードでは2倍のトークンが使用されます
- `LLM_TEMPERATURE`: デフォルト0.2（分析の一貫性のため）

## 🎯 使用例

### NVIDIA決算マーケット（Deepモード）

```bash
./run_simple.sh "https://polymarket.com/event/nvda-quarterly-earnings-nongaap-eps-11-19-2025-1pt25" deep neutral
```

### ロシア・ウクライナ停戦マーケット（Deep + Devil's Advocate）

```bash
./run_simple.sh "https://polymarket.com/event/russia-x-ukraine-ceasefire-in-2025" deep devils_advocate
```

## 💡 ヒント

- **Quickモード**: 迅速な分析が必要な場合
- **Deepモード**: より詳細で包括的な分析が必要な場合
- **Devil's Advocate**: 反証を重視した分析が必要な場合

Deepモードは時間がかかりますが、より正確で包括的な分析を提供します。

