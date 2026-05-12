import os
import requests
import json
import hmac
import hashlib
import base64
import urllib.parse
import time
import glob

def generate_sign(secret, timestamp):
    secret_enc = secret.encode('utf-8')
    string_to_sign = f'{timestamp}\n{secret}'
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return sign

def send_markdown_to_dingtalk(webhook, secret, title, text):
    timestamp = str(round(time.time() * 1000))
    sign = generate_sign(secret, timestamp)
    url = f'{webhook}&timestamp={timestamp}&sign={sign}'
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": text
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def get_latest_file(pattern):
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getctime)

def main():
    webhook = os.environ.get('DINGTALK_WEBHOOK')
    secret = os.environ.get('DINGTALK_SECRET')
    if not webhook or not secret:
        raise ValueError("请设置 DINGTALK_WEBHOOK 和 DINGTALK_SECRET")

    # 获取最新的报告文件
    report_path = get_latest_file("reports/report_*.md")
    if not report_path:
        raise FileNotFoundError("未找到报告文件")
    with open(report_path, "r", encoding="utf-8") as f:
        report_md = f.read()

    # 获取最新的分析文件（可能不存在，如果 DeepSeek 步骤失败）
    analysis_path = get_latest_file("reports/analysis_*.txt")
    analysis_text = ""
    if analysis_path:
        with open(analysis_path, "r", encoding="utf-8") as f:
            analysis_text = f.read()
    else:
        analysis_text = "⚠️ 今日 DeepSeek 分析未生成，请检查 API 配置。"

    # 合并消息（钉钉 Markdown 长度限制 20000 字符，通常够用）
    final_markdown = f"""# 📡 半导体做空日报 + AI 深度分析

## 📊 原始监控数据
{report_md}

---

## 🤖 DeepSeek 分析师解读
{analysis_text}

---
> 数据自动采集 | AI 分析仅供参考，不构成投资建议
"""
    # 发送
    res = send_markdown_to_dingtalk(webhook, secret, "半导体做空信号 + AI分析", final_markdown)
    print("钉钉响应:", res)
    if res.get('errcode') != 0:
        raise Exception(f"发送失败: {res.get('errmsg')}")

if __name__ == "__main__":
    main()
