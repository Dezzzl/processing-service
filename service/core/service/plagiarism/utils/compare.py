from .heskell_algorithm import heskell_similarity
from .hirschberg_algorithm import hirschberg_similarity


def compare_codes(tokens_a, tokens_b):
    sim_heskell = heskell_similarity(tokens_a, tokens_b)
    sim_hirschberg = hirschberg_similarity(tokens_a, tokens_b)
    avg = (sim_heskell + sim_hirschberg) / 2
    return {
        "heskell": round(sim_heskell, 2),
        "hirschberg": round(sim_hirschberg, 2),
        "average": round(avg, 2)
    }
