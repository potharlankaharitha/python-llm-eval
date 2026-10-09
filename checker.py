def is_valid_response(response):
    if not response or len(response.strip()) < 10:
        return False, "Empty or too short"
    if response.count("...") > 3:
        return False, "Contains too many ellipses"
    return True, "Valid"

def score_response(response):
    # Simple scoring logic for LLM eval
    score = 0
    if len(response.split()) > 20: score += 1
    if "." in response: score += 1
    if not response.isupper(): score += 1
    return score  # out of 3
