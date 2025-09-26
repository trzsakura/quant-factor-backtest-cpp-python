# strategy/multi_factor_strategy.py
import pandas as pd
import numpy as np

def rank_and_combine_factors(factor_dict):
    """
    对每个因子做排序（rank），然后等权合成综合得分
    factor_dict: { '000001': {'momentum': [...], 'volatility': [...], ...}, ... }
    """
    # 所有股票代码
    codes = list(factor_dict.keys())
    # 所有日期（取交集）
    dates = sorted(set.intersection(*[set(fac['momentum'].index) for fac in factor_dict.values()]))

    # 查看单个股票的索引
    # for code, fac in list(factor_dict.items())[:1]:  # 只看第一只股票
    #     print(f"{code} 的动量因子索引:")
    #     print(fac['momentum'].index)
    #     break
    
    selected_stocks = []

    for date in dates:
        print("date:", date)
        scores = []
        valid_codes = []

        for code in codes:
            fac = factor_dict[code]
            if date not in fac['momentum'].index:
                continue

            # 获取因子值
            momentum = fac['momentum'][date]
            volatility = fac['volatility'][date]
            volume_ratio = fac['volume_ratio'][date]

            # 标准化（用 rank 避免异常值影响）
            # 动量：越高越好
            # 波动率：越低越好（反转）
            # 成交量：越高越好

            score = (
                1.0 * momentum +        # 动量正向
                -0.5 * volatility +     # 波动率负向
                0.3 * volume_ratio      # 成交量正向
            )
            scores.append(score)
            valid_codes.append(code)

        # 按得分排序，选 top 2
        ranked = sorted(zip(valid_codes, scores), key=lambda x: x[1], reverse=True)
        top2 = [item[0] for item in ranked[:2]]
        selected_stocks.append({
            'date': date,
            'selected': top2
        })

    return pd.DataFrame(selected_stocks)