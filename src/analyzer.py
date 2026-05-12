import pandas as pd

def rate_us10y(val):
    if val is None:
        return 'unknown'
    pct = val * 100
    if pct < 4.3:
        return 'normal'
    if pct < 4.7:
        return 'warning'
    if pct < 5.0:
        return 'high_risk'
    return 'systemic'

def rate_sox_relative(relative, weak_days):
    if relative is None:
        return 'unknown'
    # 过热风险（跑赢过多）
    if relative > 25:
        return 'systemic'
    if relative > 18:
        return 'high_risk'
    if relative > 12:
        return 'warning'
    # 跑输风险
    if relative < -12:
        return 'systemic'
    if relative < -7:
        return 'high_risk'
    if relative < -3:
        return 'warning'
    return 'normal'

def rate_vix(val):
    if val is None:
        return 'unknown'
    if val < 18:
        return 'normal'
    if val < 25:
        return 'warning'
    if val < 35:
        return 'high_risk'
    return 'systemic'

def rate_usdjpy(val):
    if val is None:
        return 'unknown'
    if val > 160:
        return 'normal'
    if val > 155:
        return 'warning'
    if val > 148:
        return 'high_risk'
    return 'systemic'

def rate_japan10y(val):
    if val is None:
        return 'unknown'
    if val < 1.5:
        return 'normal'
    if val < 2.0:
        return 'warning'
    if val < 2.3:
        return 'high_risk'
    return 'systemic'

def rate_nvidia_growth(val):
    if val is None:
        return 'unknown'
    if val >= 80:
        return 'normal'
    if val >= 50:
        return 'warning'
    if val >= 25:
        return 'high_risk'
    return 'systemic'

def rate_cloud_capex(val):
    if val is None:
        return 'unknown'
    if val >= 25:
        return 'normal'
    if val >= 10:
        return 'warning'
    if val >= 0:
        return 'high_risk'
    return 'systemic'

def rate_fed_cut(val_str):
    mapping = {
        '>2': 'normal',
        '1': 'warning',
        '0': 'high_risk',
        'rate_hike': 'systemic'
    }
    return mapping.get(val_str, 'unknown')

def rate_ai_revenue(val_str):
    mapping = {
        'high_growth': 'normal',
        'slowing': 'warning',
        'capex_exceed': 'high_risk',
        'failed': 'systemic'
    }
    return mapping.get(val_str, 'unknown')

def rate_market_sentiment(val_str):
    mapping = {
        'rational': 'normal',
        'fomo': 'warning',
        'junk_ai_surge': 'high_risk',
        'mania': 'systemic'
    }
    return mapping.get(val_str, 'unknown')

def analyze(daily, fund_df):
    score_map = {'normal':0, 'warning':1, 'high_risk':2, 'systemic':3, 'unknown':0}
    results = {}

    # 日频
    results['us10y'] = {'value': daily.get('us10y'), 'level': rate_us10y(daily.get('us10y'))}
    results['sox_relative'] = {'value': daily.get('sox_relative'), 'level': rate_sox_relative(daily.get('sox_relative'), daily.get('weak_days', 0))}
    results['vix'] = {'value': daily.get('vix'), 'level': rate_vix(daily.get('vix'))}
    results['usdjpy'] = {'value': daily.get('usdjpy'), 'level': rate_usdjpy(daily.get('usdjpy'))}
    results['japan10y'] = {'value': daily.get('japan10y'), 'level': rate_japan10y(daily.get('japan10y'))}

    # 低频
    if fund_df is not None and not fund_df.empty:
        latest = fund_df.iloc[-1]
        results['nvidia_growth'] = {'value': latest.get('nvidia_growth'), 'level': rate_nvidia_growth(latest.get('nvidia_growth'))}
        results['cloud_capex_growth'] = {'value': latest.get('cloud_capex_growth'), 'level': rate_cloud_capex(latest.get('cloud_capex_growth'))}
        results['fed_rate_cut'] = {'value': latest.get('fed_rate_cut'), 'level': rate_fed_cut(latest.get('fed_rate_cut'))}
        results['ai_revenue_status'] = {'value': latest.get('ai_revenue_status'), 'level': rate_ai_revenue(latest.get('ai_revenue_status'))}
        results['market_sentiment'] = {'value': latest.get('market_sentiment'), 'level': rate_market_sentiment(latest.get('market_sentiment'))}
    else:
        for col in ['nvidia_growth','cloud_capex_growth','fed_rate_cut','ai_revenue_status','market_sentiment']:
            results[col] = {'value': None, 'level': 'normal'}

    total_score = sum(score_map.get(v['level'], 0) for v in results.values())
    signal = 'SELL_SHORT' if total_score >= 6 else 'NO_SIGNAL'
    return results, total_score, signal
