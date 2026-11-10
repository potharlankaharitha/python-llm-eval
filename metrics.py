# LLM Evaluation Metrics - BLEU, ROUGE, Accuracy, F1
# Used to compare LLM response vs reference answer
import re
from collections import Counter

def _tokenize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', ' ', text)
    return [w for w in text.split() if w]

def _ngrams(tokens, n):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)] if len(tokens) >= n else []

def calculate_relevance_score(response, expected_keywords):
    """Checks if LLM response contains expected keywords"""
    response_lower = response.lower()
    matched = [kw for kw in expected_keywords if kw.lower() in response_lower]
    score = len(matched) / len(expected_keywords) if expected_keywords else 0
    return {"score": round(score, 2), "matched_keywords": matched}

def check_hallucination_risk(response):
    """Simple heuristic to flag potential hallucination"""
    risky_phrases = ["as an AI", "I don't know", "I'm not sure", "100% guaranteed"]
    flags = [p for p in risky_phrases if p.lower() in response.lower()]
    return {"has_risk": len(flags) > 0, "flags": flags}

def evaluate_length_quality(text, min_words=10, max_words=150):
    """Checks if response length is ideal for evaluation"""
    wc = len(text.split())
    if wc < min_words:
        return "Too short - needs more detail"
    if wc > max_words:
        return "Too long - needs to be concise"
    return "Good length"

def bleu_score(candidate, reference, max_n=2):
    """Simplified BLEU - n-gram precision"""
    cand_tokens = _tokenize(candidate)
    ref_tokens = _tokenize(reference)
    if not cand_tokens:
        return 0.0
    scores = []
    for n in range(1, max_n+1):
        cand_ng = Counter(_ngrams(cand_tokens, n))
        ref_ng = Counter(_ngrams(ref_tokens, n))
        overlap = sum((cand_ng & ref_ng).values())
        total = sum(cand_ng.values())
        scores.append(overlap / total if total else 0)
    # Brevity penalty
    bp = 1.0 if len(cand_tokens) >= len(ref_tokens) else len(cand_tokens) / max(1, len(ref_tokens))
    avg = sum(scores) / len(scores) if scores else 0
    return round(bp * avg, 3)

def rouge_score(candidate, reference, n=1):
    """Simplified ROUGE - n-gram recall"""
    cand_tokens = _tokenize(candidate)
    ref_tokens = _tokenize(reference)
    cand_ng = Counter(_ngrams(cand_tokens, n))
    ref_ng = Counter(_ngrams(ref_tokens, n))
    overlap = sum((cand_ng & ref_ng).values())
    total_ref = sum(ref_ng.values())
    return round(overlap / total_ref if total_ref else 0, 3)

def f1_score(candidate, reference):
    """Word-level Precision, Recall, F1"""
    cand = set(_tokenize(candidate))
    ref = set(_tokenize(reference))
    if not cand or not ref:
        return {"precision": 0, "recall": 0, "f1": 0}
    tp = len(cand & ref)
    precision = tp / len(cand)
    recall = tp / len(ref)
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
    return {"precision": round(precision, 3), "recall": round(recall, 3), "f1": round(f1, 3)}

def accuracy_score(predictions, ground_truth):
    """Exact match accuracy for list of predictions"""
    if len(predictions) != len(ground_truth):
        return {"error": "Length mismatch"}
    correct = sum(1 for p, g in zip(predictions, ground_truth) if str(p).strip().lower() == str(g).strip().lower())
    return {"total": len(ground_truth), "correct": correct, "accuracy": round(correct / max(1, len(ground_truth)), 3)}

def compare_responses(response_a, response_b, reference, question=""):
    """Compare 2 LLM responses - like Alignerr task! Returns winner"""
    score_a = bleu_score(response_a, reference) + rouge_score(response_a, reference)
    f1_a = f1_score(response_a, reference)["f1"]
    score_b = bleu_score(response_b, reference) + rouge_score(response_b, reference)
    f1_b = f1_score(response_b, reference)["f1"]
    total_a = round(score_a + f1_a, 3)
    total_b = round(score_b + f1_b, 3)
    winner = "A" if total_a > total_b else "B" if total_b > total_a else "Tie"
    return {"response_a_score": total_a, "response_b_score": total_b, "winner": winner, "reason": f"Winner based on BLEU+ROUGE+F1 vs reference"}

# Example test
if __name__ == "__main__":
    resp = "Python is a programming language used for AI and LLM evaluation"
    ref = "Python is a programming language used for AI"
    print("BLEU:", bleu_score(resp, ref))
    print("ROUGE:", rouge_score(resp, ref))
    print("F1:", f1_score(resp, ref))
    print("Relevance:", calculate_relevance_score(resp, ["Python", "AI", "LLM"]))
    print("Hallucination:", check_hallucination_risk(resp))
    print("Length:", evaluate_length_quality(resp))
    print("Compare:", compare_responses("Python is great for AI", "Python is a snake", ref))
