import os

def generate_report(results, score, signal, regime, date):
    os.makedirs("reports", exist_ok=True)

    path = f"reports/report_{date}.md"

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Semiconductor Risk Report - {date}\n\n")

        f.write(f"**Market Regime:** {regime}\n\n")
        f.write(f"**Risk Score:** {score:.2f}\n\n")
        f.write(f"**Signal:** {signal}\n\n")

        f.write("| Metric | Value |\n|---|---|\n")

        for k, v in results.items():
            f.write(f"| {k} | {v} |\n")

    return path
