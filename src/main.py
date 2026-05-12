import pandas as pd
from fetcher import fetch_daily_indicators
from analyzer import analyze
from reporter import generate_report

def main():
    daily = fetch_daily_indicators()
    # 读取低频数据，若无则创建默认
    try:
        fund = pd.read_csv('data/fundamental_indicators.csv')
    except:
        fund = pd.DataFrame([{
            'date':'2025-01-01','nvidia_growth':85,'cloud_capex_growth':30,
            'fed_rate_cut':'>2','ai_revenue_status':'high_growth','market_sentiment':'rational'
        }])
        fund.to_csv('data/fundamental_indicators.csv', index=False)
    results, total_score, signal = analyze(daily, fund)
    generate_report(results, total_score, signal, daily['date'])
    # 保存每日原始数据
    daily_df = pd.DataFrame([daily])
    daily_df.to_csv('data/daily_indicators.csv', mode='a', header=not pd.io.common.file_exists('data/daily_indicators.csv'), index=False)
    print(f"Signal: {signal} | Score: {total_score}")

if __name__ == '__main__':
    main()
