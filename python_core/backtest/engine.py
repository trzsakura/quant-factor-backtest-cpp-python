# backtest/engine.py
import pandas as pd
import numpy as np

def run_backtest(selected_df, data_dict, initial_capital=100000):
    """
    简单回测：等权买入 top 2，持有5天，换仓
    """
    capital = initial_capital
    position = {}  # 当前持仓 {code: shares}
    equity_curve = []

    # 把 selected_df 按日期索引
    selected_dict = selected_df.set_index('date')['selected'].to_dict()

    # 所有日期排序
    # all_dates = sorted(data_dict[list(data_dict.keys())[0]]['trade_date'])
    all_dates = sorted(data_dict[list(data_dict.keys())[0]].index)
    if len(all_dates) == 0:
        print("all_dates列表为空")
    else:
        print(f"列表有 {len(all_dates)} 个元素")
    
    for i, current_date in enumerate(all_dates):
        if current_date not in selected_dict:
            continue

        # 每5天调仓
        if i % 5 != 0:
            continue

        # 卖出所有持仓（简化：按当日收盘价卖出）
        for code, shares in position.items():
            price = data_dict[code].loc[current_date, 'close']
            capital += shares * price
        position = {}

        # 买入新股票（等权）
        buy_list = selected_dict[current_date]
        if len(buy_list) == 0:
            continue

        per_stock_capital = capital / len(buy_list)
        for code in buy_list:
            try:
                # price = data_dict[code].set_index('trade_date').loc[current_date, 'close']
                price = data_dict[code].loc[current_date, 'close']
                shares = int(per_stock_capital / price)
                position[code] = shares
                # print("code:", code, ", shares:", shares)
                capital -= shares * price
            except KeyError:
                continue  # 股票停牌等

        # 记录现金+股票净值
        portfolio_value = capital
        for code, shares in position.items():
            price = data_dict[code].loc[current_date, 'close']
            portfolio_value += shares * price
        print("portfolio_value:", portfolio_value)

        equity_curve.append({
            'date': current_date,
            'value': portfolio_value
        })

    return pd.DataFrame(equity_curve)