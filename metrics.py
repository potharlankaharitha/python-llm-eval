# LLM Evaluation Metrics - Relevant to this role

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

# Example test
if __name__ == "__main__":
    resp = "Python is a programming language used for AI and LLM evaluation"
    print(calculate_relevance_score(resp, ["Python", "AI", "LLM"]))
    print(check_hallucination_risk(resp))
    print(evaluate_length_quality(resp))
