# utils/data_loader.py
import os
import pandas as pd
import tushare as ts
from datetime import datetime

# 设置token为环境变量
def load_stock_data(code, start_date="20200101", end_date="20230101"):
    """从 Tushare 获取单只股票数据（需设置 TUSHARE_TOKEN 环境变量）"""
    # 设置 Tushare Token
    token = os.getenv('TUSHARE_TOKEN')
    if not token:
        raise EnvironmentError("TUSHARE_TOKEN environment variable not set")
    
    # 转换股票代码格式 (600000 -> 600000.SH)
    if code.startswith('6'):
        ts_code = f"{code}.SH"
    else:
        ts_code = f"{code}.SZ"
    
    # 调用 Tushare 接口
    pro = ts.pro_api(token)
    df = pro.daily(
        ts_code=ts_code,
        start_date=start_date,
        end_date=end_date
    )
    
    # 处理数据
    if df.empty:
        return None
    
    # df = df[['trade_date', 'close', 'vol']]
    # df.columns = ['date', 'close', 'volume']
    # df['date'] = pd.to_datetime(df['date'])
    # df = df.sort_values('date').reset_index(drop=True)
    
    return df

def load_all_stocks(codes, start_date="20200101", end_date="20230101"):
    """加载多只股票数据，返回字典"""
    data_dict = {}
    for code in codes:
        print(f"正在加载 {code}...")
        df = load_stock_data(code, start_date, end_date)
        if df is not None:
            df['trade_date'] = pd.to_datetime(df['trade_date'])
            df["date"] = df['trade_date']
            df.set_index('trade_date', inplace=True)
            df = df.sort_index()
            data_dict[code] = df
    return data_dict

def save_all_stocks_to_csv(data_dict, output_dir="data"):
    """
    将多个股票数据合并保存到多个CSV文件
    
    参数:
    data_dict: 股票数据字典，格式 {股票代码: DataFrame}
    output_file: 输出文件名（默认为"all_stocks_data.csv"）
    output_dir: 输出目录（默认为"stock_data"）
    """
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 为每个股票保存CSV文件
    for code, df in data_dict.items():
        # 生成文件名（包含当前时间）
        filename = f"{output_dir}/{code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # 使用pandas直接保存
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"已保存 {code} 数据到 {filename}")

def save_all_stocks_to_single_csv(data_dict, output_file="all_stocks_data.csv", output_dir="data"):
    """
    将多个股票数据合并保存到单个CSV文件
    
    参数:
    data_dict: 股票数据字典，格式 {股票代码: DataFrame}
    output_file: 输出文件名（默认为"all_stocks_data.csv"）
    output_dir: 输出目录（默认为"stock_data"）
    """
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 构建完整文件路径
    full_path = os.path.join(output_dir, output_file)
    
    # 创建空列表用于存储所有股票的数据
    all_data = []
    
    # 为每个股票添加股票代码标识并添加到列表
    for code, df in data_dict.items():
        # 添加股票代码列
        df_with_code = df.copy()
        df_with_code['stock_code'] = code
        
        # 添加到总列表
        all_data.append(df_with_code)
    
    # 合并所有股票数据
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # 保存到CSV文件
        combined_df.to_csv(full_path, index=False, encoding='utf-8-sig')
        
        print(f"所有股票数据已合并保存到: {full_path}")
        print(f"总数据行数: {len(combined_df)}")
        print(f"股票数量: {len(data_dict)}")
        print(f"列: {list(combined_df.columns)}")
    else:
        print("没有数据可保存")

# stocks = ['600000', '000001', '600036']
# data = load_all_stocks(stocks, start_date="20230101", end_date="20231231")
# save_all_stocks_to_csv(data)