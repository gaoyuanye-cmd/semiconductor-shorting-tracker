import os
import requests
import glob
from datetime import datetime

def get_report():
    files = glob.glob("reports/*.md")
    return max(files, key=os.path.getctime)

def main():

    api_key = os.environ["DEEPSEEK_API_KEY"]

    report = open(get_report(), "r", encoding="utf-8").read()

    prompt = f"""
你是量化对冲基金分析师。

基于以下报告：

{report}

请回答：
1. 当前市场regime
2. 是否适合做空（必须：适合/观望/不适合）
3. 风险来源
4. 止损逻辑
"""

    res = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
    )

    out = res.json()["choices"][0]["message"]["content"]

    path = f"reports/analysis_{datetime.today().date()}.txt"
    open(path, "w", encoding="utf-8").write(out)

if __name__ == "__main__":
    main()
