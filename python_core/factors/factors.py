# factors/momentum.py
from factors.factor_factory import register_factor
import numpy as np

@register_factor("momentum")  # 这个装饰器会自动执行注册
def momentum_factor(df, window=20):
    """动量因子计算"""
    return df['close'].pct_change(window).dropna()

@register_factor("volatility")
def volatility_factor(df, window=20):
    """波动率因子"""
    log_ret = np.log(df['close'] / df['close'].shift(1))
    return log_ret.rolling(window).std().dropna()

@register_factor("volume_ratio")
def volume_ratio_factor(df, window=20):
    """成交量比率"""
    avg_vol = df['vol'].rolling(window).mean()
    return (df['vol'] / avg_vol).dropna()