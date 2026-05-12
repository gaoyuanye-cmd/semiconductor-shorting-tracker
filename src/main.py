import pandas as pd
from fetcher import fetch_daily_indicators
from analyzer import weighted_score
from regime import detect_regime
from signal import generate_signal
from reporter import generate_report

def main():

    data = fetch_daily_indicators()

    regime = detect_regime(
        data["vix"],
        data["us10y"],
        data["sox_relative_z"]
    )

    score = abs(data["sox_relative_z"]) + (data["vix"] / 20)

    signal = generate_signal(score, regime)

    generate_report(data, score, signal, regime, data["date"])

    print("DONE:", regime, score, signal)

if __name__ == "__main__":
    main()
