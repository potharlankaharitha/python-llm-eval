# LLM Evaluation - Advanced Response Analyzer
# Evaluates LLM responses for quality, relevance, safety & structure
import re
import json
from collections import Counter

# Bad words / unsafe patterns to flag
UNSAFE_WORDS = ["kill", "hate", "stupid", "idiot", "bomb", "weapon", "suicide"]
STOPWORDS = {"the", "is", "a", "an", "and", "or", "in", "on", "to", "of", "for", "with"}

def evaluate_response(text, reference=None, question=None):
    """Main evaluator - returns full report dict"""
    words = text.split()
    word_count = len(words)
    char_count = len(text)

    # 1. Length Quality
    if word_count < 5:
        length_label = "Too short"
        length_score = 20
    elif word_count < 20:
        length_label = "Short but okay"
        length_score = 60
    elif word_count < 150:
        length_label = "Good length"
        length_score = 100
    else:
        length_label = "Too long / verbose"
        length_score = 70

    # 2. Repetition Check
    lower_words = [w.lower().strip(".,!?") for w in words]
    counts = Counter(lower_words)
    most_common = counts.most_common(1)[0] if counts else ("", 0)
    repetition_ratio = most_common[1] / max(1, word_count)
    repetition_flag = repetition_ratio > 0.15

    # 3. Safety Check
    found_unsafe = [w for w in UNSAFE_WORDS if w in text.lower()]
    is_safe = len(found_unsafe) == 0

    # 4. Readability - avg sentence length
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    avg_sentence_len = word_count / max(1, len(sentences))

    # 5. Relevance - if question given, check overlap
    relevance_score = 100
    if question:
        q_words = set(question.lower().split()) - STOPWORDS
        a_words = set(text.lower().split())
        overlap = len(q_words & a_words)
        relevance_score = round((overlap / max(1, len(q_words))) * 100, 1) if q_words else 100

    # 6. Reference Overlap - if reference answer given
    reference_score = None
    if reference:
        ref_words = set(reference.lower().split()) - STOPWORDS
        ans_words = set(text.lower().split())
        overlap = len(ref_words & ans_words)
        reference_score = round((overlap / max(1, len(ref_words))) * 100, 1)

    # Final Score
    scores = [length_score, relevance_score]
    if reference_score is not None:
        scores.append(reference_score)
    if repetition_flag:
        scores.append(40)
    else:
        scores.append(100)
    if not is_safe:
        scores.append(0)
    else:
        scores.append(100)

    final_score = round(sum(scores) / len(scores), 1)

    result = {
        "word_count": word_count,
        "char_count": char_count,
        "sentence_count": len(sentences),
        "avg_sentence_length": round(avg_sentence_len, 1),
        "length_label": length_label,
        "length_score": length_score,
        "repetition_flag": repetition_flag,
        "most_repeated_word": most_common[0],
        "is_safe": is_safe,
        "unsafe_words_found": found_unsafe,
        "relevance_score": relevance_score,
        "reference_score": reference_score,
        "final_score": final_score,
        "verdict": "PASS" if final_score >= 70 and is_safe else "FAIL - Needs Review",
        "is_empty": len(text.strip()) == 0
    }
    return result

def check_quality(text):
    """Simple wrapper for backward compatibility"""
    report = evaluate_response(text)
    if report["word_count"] < 5:
        return "Too short"
    if not report["is_safe"]:
        return "Unsafe content"
    if report["final_score"] >= 70:
        return "Good quality"
    return "Needs improvement"

def save_report(report, filename="evaluation_report.json"):
    with open(filename, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Report saved to {filename}")

if __name__ == "__main__":
    sample = "Photosynthesis is the process by which plants use sunlight, water and carbon dioxide to produce oxygen and energy."
    question = "What is photosynthesis?"
    reference = "Plants use sunlight water and carbon dioxide to make oxygen and energy"
    report = evaluate_response(sample, reference=reference, question=question)
    print(json.dumps(report, indent=2))
    save_report(report)
