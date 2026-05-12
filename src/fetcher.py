import yfinance as yf
import pandas as pd
from pandas_datareader import data as pdr
from datetime import datetime, timedelta

def fetch_daily_indicators():
    end = datetime.today()
    start = end - timedelta(days=60)
    today = end.strftime('%Y-%m-%d')

    # US10Y (^TNX) -> 收益率百分比
    tnx = yf.Ticker("^TNX")
    us10y = tnx.history(start=start, end=end)['Close'].iloc[-1] / 100

    # SOX & QQQ
    sox = yf.Ticker("^SOX").history(start=start, end=end)['Close']
    qqq = yf.Ticker("QQQ").history(start=start, end=end)['Close']
    sox_latest, qqq_latest = sox.iloc[-1], qqq.iloc[-1]
    sox_ret = (sox.iloc[-1] / sox.iloc[-21] - 1) * 100 if len(sox) >= 21 else 0
    qqq_ret = (qqq.iloc[-1] / qqq.iloc[-21] - 1) * 100 if len(qqq) >= 21 else 0
    sox_relative = sox_ret - qqq_ret

    # 连续弱势天数（最近5日）
    weak_days = 0
    for i in range(1, min(6, len(sox)-1)):
        if (sox.iloc[-i] / sox.iloc[-i-1]) < (qqq.iloc[-i] / qqq.iloc[-i-1]):
            weak_days += 1
        else:
            break

    # VIX
    vix = yf.Ticker("^VIX").history(start=start, end=end)['Close'].iloc[-1]

    # USDJPY
    usdjpy = yf.Ticker("JPY=X").history(start=start, end=end)['Close'].iloc[-1]

    # 日本10年国债（FRED）
    try:
        japan10y = pdr.DataReader("IRLTLT01JPM156N", "fred", start, end)['IRLTLT01JPM156N'].iloc[-1]
    except:
        japan10y = None

    return {
        'date': today,
        'us10y': us10y,
        'sox_relative': sox_relative,
        'weak_days': weak_days,
        'vix': vix,
        'usdjpy': usdjpy,
        'japan10y': japan10y
    }
