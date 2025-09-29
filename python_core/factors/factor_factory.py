# factors/factor_factory.py
FACTOR_REGISTRY = {}  # 全局注册表（就像一个因子超市）

def register_factor(name):
    """注册装饰器：把因子函数"登记"到超市里"""
    def decorator(func):  # func 就是被装饰的因子函数
        FACTOR_REGISTRY[name] = func  # 把函数存入注册表
        return func  #原样返回函数（不影响正常使用）
    return decorator