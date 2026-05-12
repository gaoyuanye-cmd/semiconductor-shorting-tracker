import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from transformer import rolling_zscore

def fetch_daily_indicators():
    end = datetime.today()
    start = end - timedelta(days=120)

    today = end.strftime('%Y-%m-%d')

    sox = yf.Ticker("^SOX").history(start=start, end=end)['Close']
    qqq = yf.Ticker("QQQ").history(start=start, end=end)['Close']
    vix = yf.Ticker("^VIX").history(start=start, end=end)['Close']
    usdjpy = yf.Ticker("JPY=X").history(start=start, end=end)['Close']
    tnx = yf.Ticker("^TNX").history(start=start, end=end)['Close']

    sox_ret = sox.pct_change().dropna()
    qqq_ret = qqq.pct_change().dropna()

    sox_z = rolling_zscore(sox_ret)
    qqq_z = rolling_zscore(qqq_ret)

    sox_relative_z = sox_z - qqq_z

    return {
        "date": today,
        "sox_relative_z": sox_relative_z,
        "vix": vix.iloc[-1],
        "us10y": tnx.iloc[-1] / 100,
        "usdjpy": usdjpy.iloc[-1],
    }
