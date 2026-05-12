import pandas as pd

def rate_us10y(val):
    if val < 0.043: return 'normal'
    if val < 0.047: return 'warning'
    if val < 0.05: return 'high_risk'
    return 'systemic'

def rate_sox(relative, weak_days):
    if relative > 0: return 'normal'
    if weak_days < 5: return 'warning'
    if weak_days < 20: return 'high_risk'
    return 'systemic'

def rate_vix(val):
    if val < 18: return 'normal'
    if val < 25: return 'warning'
    if val < 40: return 'high_risk'
    return 'systemic'

def rate_usdjpy(val):
    if val > 160: return 'normal'
    if val > 155: return 'warning'
    if val >= 148: return 'high_risk'
    return 'systemic'

def rate_japan10y(val):
    if val is None: return 'unknown'
    if val < 1.5: return 'normal'
    if val < 2.0: return 'warning'
    if val < 2.3: return 'high_risk'
    return 'systemic'

def rate_fundamental(value, col_name):
    # 处理低频指标映射
    mapping = {
        'nvidia_growth': {80: 'normal', 50: 'warning', 40: 'high_risk', 25: 'systemic'},
        'cloud_capex_growth': {25: 'normal', 10: 'warning', 0: 'high_risk', -1: 'systemic'},
        'fed_rate_cut': {'>2':'normal', '1':'warning', '0':'high_risk', 'rate_hike':'systemic'},
        'ai_revenue_status': {'high_growth':'normal', 'slowing':'warning', 'capex_exceed':'high_risk', 'failed':'systemic'},
        'market_sentiment': {'rational':'normal', 'fomo':'warning', 'junk_ai_surge':'high_risk', 'mania':'systemic'}
    }
    m = mapping.get(col_name, {})
    if col_name in ['nvidia_growth', 'cloud_capex_growth']:
        for threshold, level in sorted(m.items(), reverse=True):
            if value >= threshold:
                return level
        return 'systemic'
    else:
        return m.get(value, 'unknown')

def analyze(daily, fund_df):
    latest = fund_df.iloc[-1]
    results = {}
    score_map = {'normal':0, 'warning':1, 'high_risk':2, 'systemic':3}

    # 日频
    results['us10y'] = {'value': daily['us10y'], 'level': rate_us10y(daily['us10y'])}
    results['sox_relative'] = {'value': daily['sox_relative'], 'level': rate_sox(daily['sox_relative'], daily['weak_days'])}
    results['vix'] = {'value': daily['vix'], 'level': rate_vix(daily['vix'])}
    results['usdjpy'] = {'value': daily['usdjpy'], 'level': rate_usdjpy(daily['usdjpy'])}
    results['japan10y'] = {'value': daily['japan10y'], 'level': rate_japan10y(daily['japan10y'])}

    # 低频
    for col in ['nvidia_growth', 'cloud_capex_growth', 'fed_rate_cut', 'ai_revenue_status', 'market_sentiment']:
        level = rate_fundamental(latest[col], col)
        results[col] = {'value': latest[col], 'level': level}

    total_score = sum(score_map.get(v['level'], 0) for v in results.values())
    signal = 'SELL_SHORT' if total_score >= 6 else 'NO_SIGNAL'
    return results, total_score, signal
