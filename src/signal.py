def generate_signal(score, regime):

    if regime == "euphoria" and score > 2.3:
        return "SHORT_SETUP"

    if regime == "tightening" and score > 2.0:
        return "RISK_REDUCTION"

    if regime == "risk_off":
        return "DEFENSIVE"

    if regime == "rebound":
        return "WATCH_REBOUND"

    return "NO_ACTION"
