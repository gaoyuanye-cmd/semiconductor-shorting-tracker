WEIGHTS = {
    "sox_relative": 0.4,
    "vix": 0.25,
    "us10y": 0.2,
    "usdjpy": 0.15
}

score_map = {
    "normal": 0,
    "warning": 1,
    "high_risk": 2,
    "systemic": 3
}

def weighted_score(results):
    total = 0
    for k, v in results.items():
        if k in WEIGHTS:
            total += score_map[v["level"]] * WEIGHTS[k]
    return total
