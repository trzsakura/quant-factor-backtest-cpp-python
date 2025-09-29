# main.py
from utils.data_loader import load_all_stocks, save_all_stocks_to_csv
from factors.momentum import momentum_factor
from factors.volatility import volatility_factor
from factors.volume_ratio import volume_ratio_factor
from strategy.multi_factor_strategy import rank_and_combine_factors
from backtest.engine import run_backtest
from visualization.plot_equity import plot_equity
from config import STOCKS, START_DATE, END_DATE
from factors.factor_factory import FACTOR_REGISTRY
import factors.factors
import pandas as pd
# 配置文件（支持动态配置）
config = {
    'factors': {
        'momentum': {'window': 20},
        'volatility': {'window': 20},
        'volume_ratio': {'window': 20}  # 可以灵活开关
    },
    'backtest': {
        "slippage": 0.0005,
        "commission": 0.001
    }
}
def main():
    # 1. 加载数据
    print("正在加载股票数据...")
    file_path = "C:/Users/TRZ/Downloads/100.xlsx"
    df = pd.read_excel(file_path, dtype={'证券代码': str})
    df['证券代码'] = df['证券代码'].str.zfill(6)
    stock_code = df["证券代码"].head(50).tolist()
    data_dict = load_all_stocks(stock_code, start_date=START_DATE, end_date=END_DATE)

    # 2. 计算因子
    print("正在计算因子...")
    # factor_dict = {}
    # for code, df in data_dict.items():
    #     factor_dict[code] = {
    #         'momentum': momentum_factor(df, 20),
    #         'volatility': volatility_factor(df, 20),
    #         'volume_ratio': volume_ratio_factor(df, 20)
    #     }
    factor_dict = {}
    for code, df in data_dict.items():
        factor_dict[code] = {}
        
        for factor_name, params in config['factors'].items():
            if factor_name in FACTOR_REGISTRY:
                # 工厂模式：通过名字调用对应函数
                factor_dict[code][factor_name] = FACTOR_REGISTRY[factor_name](df, **params)
    
    # 计算未来收益，用于计算ic权重
    future_return = {}
    for code, df in data_dict.items():
        # 计算下一期收益率：(P_t+1 - P_t) / P_t
        ret = (df['close'].shift(-1) / df['close'] - 1).dropna()
        future_return[code] = ret
    
    # 3. 选股
    print("正在运行选股策略...")
    selected = rank_and_combine_factors(factor_dict, future_return)
    print("选股结果(前3天):")
    print(selected.head(3))
    
    # 4. 回测
    print("正在运行回测...")
    equity = run_backtest(selected, data_dict, config)
    
    # 5. 可视化
    print("正在绘制净值曲线...")
    plot_equity(equity)
    
    print("回测完成！")

if __name__ == "__main__":
    main()