# visualization/plot_equity.py
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd

# 设置中文字体和解决负号显示问题
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题
def plot_equity(equity_df):
    # # 在出错前添加调试代码
    # print("DataFrame 的列名:", equity_df.columns.tolist())
    # print("DataFrame 的前几行:")
    # print(equity_df.head())
    equity_df = equity_df.copy()
    equity_df['date'] = pd.to_datetime(equity_df['date'])
    equity_df = equity_df.sort_values('date')
    
    plt.figure(figsize=(12, 6))
    plt.plot(equity_df['date'], equity_df['value'], label='净资产')
    plt.title("多因子选股回测净值曲线")
    plt.xlabel("日期")
    plt.ylabel("净值")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()