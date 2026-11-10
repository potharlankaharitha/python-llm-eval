# Python LLM Eval - Response Evaluator

Evaluate LLM responses for quality, relevance, safety, hallucination & bias.
Built for LLM evaluation / Alignerr-style review tasks.

## Features
- **main.py** - Length, repetition, relevance, safety, final score (PASS/FAIL)
- **metrics.py** - BLEU, ROUGE, F1, Accuracy, Relevance, Compare 2 responses (A/B)
- **checker.py** - Validation, Safety, Hallucination detection, Bias check, Final Verdict (APPROVE / REJECT / NEEDS REVIEW)

## How to Run
```bash
python main.py
python metrics.py
python checker.py
