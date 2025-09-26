# main.py
from utils.data_loader import load_all_stocks
from factors.momentum import momentum_factor
from factors.volatility import volatility_factor
from factors.volume_ratio import volume_ratio_factor
from strategy.multi_factor_strategy import rank_and_combine_factors
from backtest.engine import run_backtest
from visualization.plot_equity import plot_equity
from config import STOCKS, START_DATE, END_DATE
import pandas as pd

def main():
    # 1. 加载数据
    print("正在加载股票数据...")
    data_dict = load_all_stocks(STOCKS, start_date=START_DATE, end_date=END_DATE)
    
    # 2. 计算因子
    print("正在计算因子...")
    factor_dict = {}
    for code, df in data_dict.items():
        factor_dict[code] = {
            'momentum': momentum_factor(df, 20),
            'volatility': volatility_factor(df, 20),
            'volume_ratio': volume_ratio_factor(df, 20)
        }

    # 查看原始数据
    # for code, df in list(data_dict.items())[:1]:
    #     print(f"{code} 的数据结构:")
    #     print(df.head())
    #     print(f"列名: {df.columns.tolist()}")
    #     print(f"索引: {df.index}")
    
    # 3. 选股
    print("正在运行选股策略...")
    selected = rank_and_combine_factors(factor_dict)
    print("选股结果（前3天）:")
    print(selected.head(3))
    
    # 4. 回测
    print("正在运行回测...")
    equity = run_backtest(selected, data_dict)
    
    # 5. 可视化
    print("正在绘制净值曲线...")
    plot_equity(equity)
    
    print("回测完成！")

if __name__ == "__main__":
    main()