# LLM Evaluation - Simple Text Analyzer
def evaluate_response(text):
    result = {
        "word_count": len(text.split()),
        "char_count": len(text),
        "is_empty": len(text.strip()) == 0
    }
    return result

def check_quality(text):
    if len(text.split()) < 5:
        return "Too short"
    return "Good length"

if __name__ == "__main__":
    sample = "This is a sample response from LLM to evaluate"
    print(evaluate_response(sample))
    print(check_quality(sample))
