import sys
sys.path.append("cpp_core/Release")  # 指向编译后的模块

try:
    import factor_core
    print("✅ C++ 模块导入成功！")
    
    # 测试数据
    prices = [10.0, 10.2, 10.1, 10.5, 10.7, 11.0, 10.9]
    ret = factor_core.calc_momentum(prices, 2)
    print("C++ 计算结果:", ret)  # 应输出 [0.1, 0.375, 0.466, 0.571, 0.488]
    
except ImportError as e:
    print("❌ 导入失败:", e)
    print("请检查编译是否成功")