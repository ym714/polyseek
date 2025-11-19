# Deep Mode Guide

Deep mode provides comprehensive analysis through a 4-step process: Planner → Critic → Follow-up → Final.

## Usage

```bash
./scripts/run_simple.sh "https://polymarket.com/event/your-market-slug" deep neutral
./scripts/run_simple.sh "https://polymarket.com/event/your-market-slug" deep devils_advocate
```

## Process

1. **Planner**: Creates analysis plan, identifies key questions and information gaps
2. **Critic**: Critically evaluates plan, identifies gaps and biases
3. **Follow-up**: Gathers additional data to fill identified gaps
4. **Final**: Comprehensive synthesis with all evidence

## Comparison

| Feature | Quick Mode | Deep Mode |
|---------|------------|-----------|
| Steps | 1 pass | 4 steps |
| Time | ~30s | ~120s |
| Tokens | 1,024 | 2,048 |
| Depth | Basic | Comprehensive |

## Output

Deep mode includes additional metadata:

```json
{
  "metadata": {
    "mode": "deep",
    "plan": ["Step 1: ...", "Step 2: ..."],
    "critique": {
      "gaps": ["Gap 1: ..."],
      "follow_up_queries": ["Query 1: ..."]
    }
  }
}
```

## Configuration

Deep mode is enabled by setting `depth="deep"`. Environment variables:
- `LLM_MAX_TOKENS`: Uses 2x tokens in deep mode
- `LLM_TEMPERATURE`: Default 0.2 for consistency
