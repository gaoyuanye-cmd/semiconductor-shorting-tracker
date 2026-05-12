# 半导体做空跟踪器

每日自动获取市场指标，结合 DeepSeek AI 分析，判断半导体做空时机，并推送到钉钉群。

## 功能
- 自动获取 US10Y、SOX/QQQ 相对强弱、VIX、USDJPY、日本10Y国债
- 手动维护低频指标（英伟达增速、云 CapEx、降息预期等）
- 双向风险评分（过热与跑输均计分）
- 每日生成 Markdown 报告
- 调用 DeepSeek API 给出专业解读
- 推送至钉钉群

## 配置
在 GitHub Secrets 中设置：
- `DEEPSEEK_API_KEY`：DeepSeek API Key
- `DINGTALK_WEBHOOK`：钉钉机器人 Webhook
- `DINGTALK_SECRET`：钉钉加签密钥
- `PAT_TOKEN`（可选，用于推送报告）

## 手动更新低频数据
编辑 `data/fundamental_indicators.csv`，按行追加最新季度数据。

## 手动运行
在 Actions 页面点击 `Run workflow`。
