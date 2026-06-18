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

#与下一任务分隔
print()

# 导入绘图库matplotlib，用于后续可视化（本段代码暂未绘图，预留绘图工具）
import matplotlib.pyplot as plt
# 筛选刷卡类型等于0的所有数据，单独存入子数据集df0
df0 = df[df['刷卡类型'] == 0]
# 获取刷卡类型为0的总乘车记录条数
total = len(df0)
# 统计早峰前出行人数：hour<7 即7点前乘车的记录数量
early = np.sum(df0['hour'] < 7)
early0=early/total*100
# 统计深夜出行人数：hour>=22 即22点及之后乘车的记录数量
late = np.sum(df0['hour'] >= 22)
late0=late/total*100
print("[任务2(a)]早峰前/深夜上车刷卡量：")
# 打印7点前早峰前出行总人次
print(f"早上7点前公共交通上车刷卡量为：{early}次，占全天{early0:.2f}%")
# 打印22点后深夜出行总人次
print(f"晚上10点后公共交通上车刷卡量为：{late}次，占全天{late0:.2f}%")
# 统计刷卡类型0各小时乘车人次，按0~23小时升序排列
# value_counts()统计每个hour出现次数；sort_index()按小时0-23从小到大排序
hour_counts = df0['hour'].value_counts().sort_index()
# 创建画布，设置尺寸 宽10英寸，高5英寸
plt.figure(figsize=(10,5))
# 遍历所有小时，自定义柱子颜色：
# 小时<7 或 >=22 → 橙色（代表早峰前、深夜时段）；其余白天时段浅蓝色
colors = ['orange' if (h < 7 or h >= 22) else 'skyblue' for h in hour_counts.index]
# 绘制柱状图：x轴小时，y轴对应乘车人次，使用上面自定义的区分颜色
plt.bar(hour_counts.index, hour_counts.values, color=colors)
# 设置图表标题、坐标轴标签
plt.title("24-hour Boarding Counts Distribution")
plt.xlabel("Hour(0~23)")
plt.ylabel("Boarding Count")
#准备图例
plt.bar(hour_counts.index,
        hour_counts.values,
        color=colors,
        label='Early & Late Highlight')

plt.legend()
# X轴刻度，间隔2小时显示，避免刻度拥挤
plt.xticks(range(0,24,2))
# 添加x，y轴网格线，方便读取数值
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.grid(axis='x', linestyle='-', alpha=0.5)
# 保存图片到代码同目录，分辨率150dpi
plt.savefig("hour_distribution.png", dpi=150)
print("[任务2(b)]已保存图像：hour_distribution.png")
# 弹出窗口展示图表
plt.show()