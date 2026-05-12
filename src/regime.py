def detect_regime(vix, us10y, sox_z):

    if vix > 25:
        return "risk_off"

    if us10y > 4.7:
        return "tightening"

    if sox_z > 2 and vix < 20:
        return "euphoria"

    if sox_z < -1 and vix < 18:
        return "rebound"

    return "neutral"
