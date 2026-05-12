# src/analyzer.py
import pandas as pd

# ======================= 单指标评级函数 =======================

def rate_us10y(val):
    """美国10年期国债收益率（单位：小数，如 0.0441 表示 4.41%）"""
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
    """
    SOX 相对 QQQ 的强弱指标（收益率差值，单位：%）
    双向风险：极度过热（泡沫末期）和持续跑输（趋势反转）
    """
    if relative is None:
        return 'unknown'
    
    # ----- 过热风险（跑赢过多）-----
    if relative > 25:
        return 'systemic'      # 极端泡沫，历史罕见
    if relative > 18:
        return 'high_risk'     # 严重超买，如当前 18.1%
    if relative > 12:
        return 'warning'       # 明显过热，开始警惕
    
    # ----- 跑输风险（弱势）-----
    if relative < -12:
        return 'systemic'      # 崩溃式跑输
    if relative < -7:
        return 'high_risk'     # 明确转弱
    if relative < -3:
        return 'warning'       # 开始跑输
    
    # 中间区域（-3% ~ +12%）视为正常区间
    return 'normal'

def rate_vix(val):
    """VIX 恐慌指数"""
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
    """美元兑日元汇率"""
    if val is None:
        return 'unknown'
    if val > 160:
        return 'normal'        # 日元弱势，风险偏好高
    if val > 155:
        return 'warning'       # 接近干预线
    if val > 148:
        return 'high_risk'     # 日元走强，套利平仓风险
    return 'systemic'          # 日元极端走强，全球风险资产承压

def rate_japan10y(val):
    """日本10年期国债收益率（%）"""
    if val is None:
        # 数据缺失时按最保守处理：假设正常（0分），但会额外提醒
        return 'unknown'
    if val < 1.5:
        return 'normal'
    if val < 2.0:
        return 'warning'
    if val < 2.3:
        return 'high_risk'
    return 'systemic'

# ---------- 低频指标评级（从 fundamental 表读取）----------
def rate_nvidia_growth(val):
    """英伟达数据中心收入同比增速（%）"""
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
    """云厂商资本开支同比增速（%）"""
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
    """美联储降息预期（字符串）"""
    mapping = {
        '>2': 'normal',
        '1': 'warning',
        '0': 'high_risk',
        'rate_hike': 'systemic'
    }
    return mapping.get(val_str, 'unknown')

def rate_ai_revenue(val_str):
    """AI商业化收入状况"""
    mapping = {
        'high_growth': 'normal',
        'slowing': 'warning',
        'capex_exceed': 'high_risk',
        'failed': 'systemic'
    }
    return mapping.get(val_str, 'unknown')

def rate_market_sentiment(val_str):
    """市场情绪"""
    mapping = {
        'rational': 'normal',
        'fomo': 'warning',
        'junk_ai_surge': 'high_risk',
        'mania': 'systemic'
    }
    return mapping.get(val_str, 'unknown')

# ======================= 主分析函数 =======================

def analyze(daily, fund_df):
    """
    输入：
        daily: dict，包含日频指标的当前值
        fund_df: DataFrame，至少有一行最新数据（列名与上面函数匹配）
    返回：
        results: dict，每个指标的评级及原始数值
        total_score: int，加权总分（此处简单相加，可后续扩展权重）
        signal: str，'SELL_SHORT' 或 'NO_SIGNAL'
    """
    # 风险分数映射
    score_map = {
        'normal': 0,
        'warning': 1,
        'high_risk': 2,
        'systemic': 3,
        'unknown': 0      # 未知当作0分，但会在报告中提示
    }
    
    results = {}
    
    # --- 日频指标 ---
    results['us10y'] = {
        'value': daily.get('us10y'),
        'level': rate_us10y(daily.get('us10y'))
    }
    
    results['sox_relative'] = {
        'value': daily.get('sox_relative'),
        'level': rate_sox_relative(daily.get('sox_relative'), daily.get('weak_days', 0))
    }
    
    results['vix'] = {
        'value': daily.get('vix'),
        'level': rate_vix(daily.get('vix'))
    }
    
    results['usdjpy'] = {
        'value': daily.get('usdjpy'),
        'level': rate_usdjpy(daily.get('usdjpy'))
    }
    
    results['japan10y'] = {
        'value': daily.get('japan10y'),
        'level': rate_japan10y(daily.get('japan10y'))
    }
    
    # --- 低频指标（取最新一行）---
    if fund_df is not None and not fund_df.empty:
        latest = fund_df.iloc[-1]
        results['nvidia_growth'] = {
            'value': latest.get('nvidia_growth'),
            'level': rate_nvidia_growth(latest.get('nvidia_growth'))
        }
        results['cloud_capex_growth'] = {
            'value': latest.get('cloud_capex_growth'),
            'level': rate_cloud_capex(latest.get('cloud_capex_growth'))
        }
        results['fed_rate_cut'] = {
            'value': latest.get('fed_rate_cut'),
            'level': rate_fed_cut(latest.get('fed_rate_cut'))
        }
        results['ai_revenue_status'] = {
            'value': latest.get('ai_revenue_status'),
            'level': rate_ai_revenue(latest.get('ai_revenue_status'))
        }
        results['market_sentiment'] = {
            'value': latest.get('market_sentiment'),
            'level': rate_market_sentiment(latest.get('market_sentiment'))
        }
    else:
        # 若没有低频数据，给默认正常值并警告
        for col in ['nvidia_growth', 'cloud_capex_growth', 'fed_rate_cut', 'ai_revenue_status', 'market_sentiment']:
            results[col] = {'value': None, 'level': 'normal'}
    
    # 计算总分（简单线性相加，后续可改为加权）
    total_score = 0
    for key, item in results.items():
        level = item['level']
        score = score_map.get(level, 0)
        total_score += score
        item['score'] = score   # 将分数存入结果，方便调试
    
    # 做空信号阈值（与 config.yaml 保持一致）
    threshold = 6
    signal = 'SELL_SHORT' if total_score >= threshold else 'NO_SIGNAL'
    
    return results, total_score, signal
