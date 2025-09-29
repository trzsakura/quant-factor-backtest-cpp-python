# strategy/multi_factor_strategy.py
import pandas as pd
import numpy as np

def ic_weighted_score(factor_dict, future_return):
    """用 IC 值作为权重"""
    ic = {}
    for code, fac in factor_dict.items():
        for name, values in fac.items():
            # 计算因子值与未来收益的皮尔逊相关系数
            corr = np.corrcoef(values, future_return[code])[0,1]
            ic[name] = ic.get(name, []) + [corr]
    # 平均 IC 作为权重
    avg_ic = {k: np.mean(v) for k, v in ic.items()}
    return avg_ic

def rank_and_combine_factors(factor_dict, future_return):
    """
    对每个因子做排序（rank），然后等权合成综合得分
    factor_dict: { '000001': {'momentum': [...], 'volatility': [...], ...}, ... }
    """
    # 所有股票代码
    codes = list(factor_dict.keys())
    # 所有日期（取交集）
    dates = sorted(set.intersection(*[set(fac['momentum'].index) for fac in factor_dict.values()]))

    # 对齐因子和未来收益日期
    for code in codes:
        fac_dates = set(factor_dict[code]['momentum'].index)
        # 收益日期
        ret_dates = set(future_return[code].index)
        # 交集
        stock_dates = fac_dates & ret_dates

        common_date = sorted(stock_dates)

        # 对齐动量因子
        factor_dict[code]['momentum'] = factor_dict[code]['momentum'].loc[common_date]
        factor_dict[code]['volatility'] = factor_dict[code]['volatility'].loc[common_date]
        factor_dict[code]['volume_ratio'] = factor_dict[code]['volume_ratio'].loc[common_date]
        # 对齐未来收益
        future_return[code] = future_return[code].loc[common_date]

    # 计算ic权重
    weights = ic_weighted_score(factor_dict, future_return)

    selected_stocks = []
    for date in dates:
        scores = []
        valid_codes = []

        for code in codes:
            fac = factor_dict[code]
            if date not in fac['momentum'].index:
                continue

            # 获取因子值, 计算ic权重
            score = 0
            for factor_name, weight in weights.items():
                score += fac[factor_name][date] * weight
            # score = (
            #     1.0 * momentum +        # 动量正向
            #     -0.5 * volatility +     # 波动率负向
            #     0.3 * volume_ratio      # 成交量正向
            # )

            scores.append(score)
            valid_codes.append(code)

        # 按得分排序，选 top 3
        ranked = sorted(zip(valid_codes, scores), key=lambda x: x[1], reverse=True)
        top3 = [item[0] for item in ranked[:3]]
        selected_stocks.append({
            'date': date,
            'selected': top3
        })

    return pd.DataFrame(selected_stocks)