import os
import requests
import json
from datetime import datetime
import glob

def call_deepseek(prompt, api_key):
    """调用 DeepSeek API（兼容 OpenAI 接口）"""
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",  # 或者 deepseek-reasoner（深度思考）
        "messages": [
            {"role": "system", "content": "你是一位专业的半导体行业分析师，擅长解读市场指标并给出做空/做多建议。请基于用户提供的报告数据，用中文给出简洁、客观的分析。重点回答：当前风险等级是否适合做空？为什么？需要关注哪些关键变化？"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 800
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def get_latest_report(report_dir="reports"):
    """获取最新的报告文件路径"""
    files = glob.glob(f"{report_dir}/report_*.md")
    if not files:
        raise FileNotFoundError("未找到任何报告文件")
    latest = max(files, key=os.path.getctime)
    return latest

def main():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("请在环境变量中设置 DEEPSEEK_API_KEY")

    # 获取最新报告路径
    report_path = get_latest_report()
    with open(report_path, "r", encoding="utf-8") as f:
        report_content = f.read()

    # 构造 prompt（将报告完整附上）
    prompt = f"以下是今天的半导体市场监控报告：\n\n{report_content}\n\n请分析：\n1. 整体风险处于什么水平？\n2. 目前是否适合做空半导体？给出明确建议（适合/观望/不适合）。\n3. 最重要的三个预警指标是什么？\n4. 短期需要关注的变量。"
    
    print("正在调用 DeepSeek API 进行分析...")
    analysis = call_deepseek(prompt, api_key)

    # 保存分析结果
    date_str = datetime.today().strftime("%Y-%m-%d")
    analysis_path = f"reports/analysis_{date_str}.txt"
    with open(analysis_path, "w", encoding="utf-8") as f:
        f.write(analysis)
    
    print(f"分析结果已保存至 {analysis_path}")

if __name__ == "__main__":
    main()
