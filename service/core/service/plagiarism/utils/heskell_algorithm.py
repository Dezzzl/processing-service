def kgrams(tokens, k=5):
    return {" ".join(tokens[i:i+k]) for i in range(len(tokens) - k + 1)}


def heskell_similarity(tokens_a, tokens_b, k=5):
    kgrams_a = kgrams(tokens_a, k)
    kgrams_b = kgrams(tokens_b, k)

    intersection = len(kgrams_a & kgrams_b)
    union = len(kgrams_a | kgrams_b)
    if union == 0:
        return 0.0
    return (intersection / union) * 100
