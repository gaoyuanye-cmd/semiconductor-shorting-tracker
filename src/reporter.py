import os

def generate_report(results, total_score, signal, date_str):
    os.makedirs('reports', exist_ok=True)
    filename = f'reports/report_{date_str}.md'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# 半导体做空报告 - {date_str}\n\n")
        f.write(f"**总分**: {total_score}  **信号**: {signal}\n\n")
        f.write("| 指标 | 数值 | 风险等级 |\n")
        f.write("|------|------|----------|\n")
        for k, v in results.items():
            val = v['value']
            if isinstance(val, float):
                val = f"{val:.4f}"
            f.write(f"| {k} | {val} | {v['level']} |\n")
    print(f"Saved {filename}")
    return filename
