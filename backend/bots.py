def analyze_performance(results):

    analysis = {}

    for algorithm, data in results.items():

        hits = data["page_hits"]
        faults = data["page_faults"]

        total = hits + faults

        if total == 0:
            hit_rate = 0
            fault_rate = 0
        else:
            hit_rate = (hits / total) * 100
            fault_rate = (faults / total) * 100

        analysis[algorithm] = {
            "page_hits": hits,
            "page_faults": faults,
            "page_hit_rate": round(hit_rate, 2),
            "page_fault_rate": round(fault_rate, 2)
        }

    min_faults = min(
        data["page_faults"]
        for data in analysis.values()
    )

    best_algorithms = [
        name for name, data in analysis.items()
        if data["page_faults"] == min_faults
    ]

    return {
        "comparison": analysis,
        "best_algorithm": best_algorithms,
        "message": (
            "The algorithm with the fewest page faults "
            "has the best performance for this input."
        )
    }
