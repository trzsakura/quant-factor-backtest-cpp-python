# factors/momentum.py
import pandas as pd
import numpy as np

def volatility_factor(df, window=20):
    """计算对数收益率标准差（波动率）"""
    log_ret = np.log(df['close'] / df['close'].shift(1))
    return log_ret.rolling(window).std().dropna()