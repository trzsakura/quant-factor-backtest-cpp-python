# factors/volume_ratio.py
import pandas as pd

def volume_ratio_factor(df, window=20):
    """计算当前成交量 / 过去 N 日均值"""
    volume_mean = df['vol'].rolling(window).mean()
    return (df['vol'] / volume_mean).dropna()