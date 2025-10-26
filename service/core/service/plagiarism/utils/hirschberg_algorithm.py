def levenshtein_distance(a: list[str], b: list[str]) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            curr[j] = min(
                prev[j] + 1,
                curr[j - 1] + 1,
                prev[j - 1] + cost
            )
        prev = curr
    return prev[-1]


def hirschberg_similarity(tokens_a, tokens_b):
    dist = levenshtein_distance(tokens_a, tokens_b)
    max_len = max(len(tokens_a), len(tokens_b))
    if max_len == 0:
        return 0.0
    return (1 - dist / max_len) * 100
