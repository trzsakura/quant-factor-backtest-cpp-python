# visualization/dashboard.py
import pandas as pd
import matplotlib as plt


def plot_dashboard(equity_df, selected_df, factor_corr):
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 净值曲线
    axes[0,0].plot(equity_df['date'], equity_df['value']/equity_df['value'].iloc[0])
    axes[0,0].set_title("净值曲线")
    
    # 选股分布
    all_stocks = [code for codes in selected_df['selected'] for code in codes]
    pd.Series(all_stocks).value_counts().head(10).plot(kind='bar', ax=axes[0,1])
    axes[0,1].set_title("被选中次数 Top 10")

    # 因子相关性
    factor_corr.plot(ax=axes[1,0], cmap='coolwarm', center=0)
    axes[1,0].set_title("因子相关性")

    # 回撤曲线
    drawdown = (equity_df['value'] / equity_df['value'].cummax() - 1)
    axes[1,1].plot(equity_df['date'], drawdown)
    axes[1,1].set_title("回撤曲线")

    plt.tight_layout()
    plt.show()