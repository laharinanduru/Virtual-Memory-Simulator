
def performance_analysis_bot(results):
    """
    Performance Analysis Bot

    Compares FIFO, LRU and Optimal page replacement
    algorithms and recommends the best performer.
    """

    # Validate input
    if not isinstance(results, dict):
        return {
            "success": False,
            "message": "Invalid simulation results."
        }

    # Support nested API results
    if isinstance(results.get("results"), dict):
        results = results["results"]

    algorithms = ["FIFO", "LRU", "Optimal"]
    comparison = []

    # Collect algorithm results
    for algorithm in algorithms:

        data = results.get(algorithm)

        if not isinstance(data, dict):
            return {
                "success": False,
                "message": f"Missing results for {algorithm}."
            }

        try:
            hits = int(data["page_hits"])
            faults = int(data["page_faults"])
        except (KeyError, TypeError, ValueError):
            return {
                "success": False,
                "message": f"Invalid metrics for {algorithm}."
            }

        if hits < 0 or faults < 0:
            return {
                "success": False,
                "message": f"Negative metrics for {algorithm}."
            }

        comparison.append({
            "algorithm": algorithm,
            "page_hits": hits,
            "page_faults": faults
        })

    # Check whether all algorithms processed
    # the same number of page references
    totals = {
        item["page_hits"] + item["page_faults"]
        for item in comparison
    }

    if len(totals) != 1 or 0 in totals:
        return {
            "success": False,
            "message": "Algorithm results have inconsistent page references."
        }

    total_references = totals.pop()

    # Calculate performance rates
    for item in comparison:
        item["page_fault_rate"] = round(
            item["page_faults"] / total_references * 100, 2
        )

        item["page_hit_rate"] = round(
            item["page_hits"] / total_references * 100, 2
        )

    # Identify the algorithm with minimum faults
    minimum_faults = min(
        item["page_faults"] for item in comparison
    )

    best_algorithms = [
        item["algorithm"]
        for item in comparison
        if item["page_faults"] == minimum_faults
    ]

    # Generate explanation
    if len(best_algorithms) == 1:
        best_algorithm = best_algorithms[0]

        explanation = (
            f"{best_algorithm} performed best because it produced "
            f"only {minimum_faults} page faults."
        )

    else:
        best_algorithm = best_algorithms

        explanation = (
            "A tie occurred between "
            + ", ".join(best_algorithms)
            + f". All produced {minimum_faults} page faults."
        )

    # Generate recommendation
    recommendation = (
        "Recommended algorithm: "
        + ", ".join(best_algorithms)
        + ". It achieved the lowest page-fault count "
        "for this simulation."
    )

    # Return complete analysis
    return {
        "success": True,
        "total_references": total_references,
        "comparison": comparison,
        "best_algorithm": best_algorithm,
        "minimum_page_faults": minimum_faults,
        "explanation": explanation,
        "recommendation": recommendation
    }


# Test the bot independently
if __name__ == "__main__":

    sample_results = {
        "FIFO": {
            "page_hits": 3,
            "page_faults": 7
        },
        "LRU": {
            "page_hits": 5,
            "page_faults": 5
        },
        "Optimal": {
            "page_hits": 7,
            "page_faults": 3
        }
    }

    result = performance_analysis_bot(sample_results)

    print("===== PERFORMANCE ANALYSIS BOT =====")

    for key, value in result.items():
        print(f"{key}: {value}")

