# factors/momentum.py
import pandas as pd
import numpy as np

def momentum_factor(df, window=20):
    """计算 N 日收益率（动量）"""
    close = df['close']
    return (close / close.shift(window) - 1).dropna()