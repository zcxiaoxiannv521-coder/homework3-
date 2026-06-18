#导入数据分析库pandas、数值计算库numpy
import pandas as pd
import numpy as np
# 读取本地IC刷卡交易csv文件，加载为DataFrame表格数据
df = pd.read_csv("ICData.csv")
#打印提示文字，输出数据集前5条完整样本，to_string去除末尾行列提示
print("数据集前5行：")
print(df.head(5).to_string())
#空一行分隔输出内容，控制台排版更清晰，与老师输出结果类似
print()
#单独提取【运营公司编号】一列，打印前5行，查看该字段数据分布
print(df[['运营公司编号']].head())
#换行打印数据集整体基础信息
print("\n基本信息：")
#df.shape返回(总行数,总列数)，shape[0]取行数，shape[1]取列数
print("行数=",df.shape[0],",","列数=",df.shape[1])
#查看每一列的数据类型，打印自带dtype:object后缀，用于检查字段格式问题
print(df.dtypes)
#将原本文本格式的【交易时间】转换为pandas标准时间格式，用于提取时间特征
df['交易时间'] = pd.to_datetime(df['交易时间'])
#从标准时间字段中提取小时（0~23），新建hour列，用于分时段客流分析（早/晚高峰）
df['hour'] = df['交易时间'].dt.hour
#计算单次乘车经过站点数量：下车站点-上车站点取绝对值，避免上下车顺序颠倒出现负数
df['ride_stops'] = abs(df['下车站点'] - df['上车站点'])
#记录清洗前与后的总数据条数，作差得到异常数据条数
before = len(df)
df = df[df['ride_stops'] != 0]
after = len(df)
print("\n构造ride_stops后删除异常记录(ride_stops==0/无运送计算)行数:", before - after)
#打印缺失值统计标题
print("\n各列缺失值数量：")
missing_count = df.isnull().sum()
#判断是否全部列缺失值都为0
if (missing_count == 0).all():
    print("无缺失值")
else:
    print(missing_count)
#执行删除缺失值（如果无缺失，这行不会改动数据）
df = df.dropna()