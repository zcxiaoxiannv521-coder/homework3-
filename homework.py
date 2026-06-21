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
# 将“交易时间”这一列从字符串类型转换为 pandas 的 datetime 时间类型
# 这样后续才能使用 .dt.hour、.dt.minute 等时间属性
df['交易时间'] = pd.to_datetime(df['交易时间'])
# 从已经转换好的 datetime 时间中提取“小时”信息
# 例如 2018/4/1 11:45:12 会提取出 11
# 新增 hour 列，用于后续统计每个小时的刷卡量
df['hour'] = df['交易时间'].dt.hour
# 计算每条乘车记录的搭乘站点数
# 用“下车站点 - 上车站点”的绝对值，避免出现负数
df['ride_stops'] = abs(df['下车站点'] - df['上车站点'])
# 记录删除异常数据前的数据总行数
before = len(df)
# 删除 ride_stops 等于 0 的记录
# 因为上下车站点相同，说明没有有效乘车距离，视为异常记录
df = df[df['ride_stops'] != 0]
# 记录删除异常数据后的数据总行数
after = len(df)
# 打印被删除的异常记录数量
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

#与下一任务分隔
print()

print("[任务3]每条线路的平均搭乘站点数及标准差(前10行)：")
def analyze_route_stops(df, route_col='线路号', stops_col='ride_stops'):
    """
    计算各线路乘客的平均搭乘站点数及其标准差
    """
    result = df.groupby(route_col)[stops_col].agg(['mean','std']).reset_index()
    result.columns = [route_col, 'mean_stops', 'std_stops']
    result = result.sort_values('mean_stops', ascending=False)
    return result
# 导入seaborn库
import seaborn as sns
# 调用自定义函数，得到每条线路的平均搭乘站点数和标准差
res = analyze_route_stops(df)
# 取平均搭乘站点数最高的前15条线路，用于后续可视化
top15 = res.head(15).copy()
# 再次按mean_stops降序排列，确保打印和画图顺序稳定
top15_sort1 = top15.sort_values('mean_stops', ascending=False)
# 重置索引，使左侧序号从0开始，避免保留原始DataFrame索引
top15_sort2 = top15_sort1.reset_index(drop=True)
# 打印Top15中的前10行，满足题目“打印结果前10行”的要求
print(top15_sort2.head(10))
# 为了让图中线路号按从小到大显示，按线路号升序重新排列
top15_sorted = top15.sort_values("线路号", ascending=True).reset_index(drop=True)
# 创建画布，设置图像宽12英寸、高7英寸
plt.figure(figsize=(12, 7))
# 设置蓝色渐变调色板，颜色数量与Top15线路数量一致
colors = sns.color_palette("Blues_d", n_colors=len(top15_sorted))
# 使用seaborn绘制横向条形图
# x轴为平均搭乘站点数，y轴为线路号
ax = sns.barplot(
    data=top15_sorted,
    x='mean_stops',
    y='线路号',
    hue='线路号',
    palette=colors,
    orient='h',
    legend=False
)
# 生成每一根柱子对应的y轴位置，用于后续误差线对齐
y_pos = np.arange(len(top15_sorted))
# 手动添加误差线，xerr表示横向误差范围
# 这里使用std_stops作为误差棒，表示各线路搭乘站点数的波动程度
plt.errorbar(
    x=top15_sorted['mean_stops'],
    y=y_pos,
    xerr=top15_sorted['std_stops'],
    fmt='none',
    ecolor='black',
    capsize=0.3,
    linewidth=1
)
# 设置图表标题
plt.title("Top 15 Routes: Mean Ride Stops (with Std Dev)")
# 设置x轴标签
plt.xlabel("Mean Ride Stops")
# 设置y轴标签
plt.ylabel("Route ID")
# 添加x轴方向网格线，方便观察平均站点数大小
plt.grid(axis='x', linestyle='-', alpha=0.3)
# 设置x轴从0开始，符合题目要求
plt.xlim(left=0)
# 设置x轴刻度为0、5、10、15、20
plt.xticks(range(0, 25, 5))
# 自动调整布局，避免标题、标签或坐标轴被遮挡
plt.tight_layout()
# 保存图像到当前目录，文件名符合题目要求
plt.savefig("route_stops.png", dpi=150, bbox_inches='tight')
# 展示图像
plt.show()
# 打印图片保存提示
print("\n[任务3]已保存图像：route_stops.png\n")

print("[任务4]高峰小时系数PHF计算结果：")
# 只保留刷卡类型为0的记录
# 题目要求后续统计均只统计“上车刷卡”记录
df0 = df[df['刷卡类型'] == 0].copy()
# 按 hour 字段分组，统计每个小时内的刷卡记录数量
# groupby('hour').size() 得到每个小时对应的刷卡量
hour_counts = df0.groupby('hour').size()
# idxmax() 返回刷卡量最大值对应的小时，即自动识别出的高峰小时
peak_hour = hour_counts.idxmax()
# max() 返回高峰小时内的总刷卡量
peak_count = hour_counts.max()
# 从 df0 中筛选出高峰小时内的所有刷卡记录
# 后面只在这个小时范围内做5分钟和15分钟粒度统计
peak_df = df0[df0['hour'] == peak_hour].copy()
# 将高峰小时内每条记录的交易时间向下取整到最近的5分钟
peak_df['time_5min'] = peak_df['交易时间'].dt.floor('5min')
# 按5分钟窗口分组，统计每个5分钟窗口内的刷卡量
five_counts = peak_df.groupby('time_5min').size()
# 找出刷卡量最大的5分钟窗口的开始时间
max_5_time = five_counts.idxmax()
# 找出高峰小时内最大5分钟刷卡量
max_5_count = five_counts.max()
# 将高峰小时内每条记录的交易时间向下取整到最近的15分钟
peak_df['time_15min'] = peak_df['交易时间'].dt.floor('15min')
# 按15分钟窗口分组，统计每个15分钟窗口内的刷卡量
fifteen_counts = peak_df.groupby('time_15min').size()
# 找出刷卡量最大的15分钟窗口的开始时间
max_15_time = fifteen_counts.idxmax()
# 找出高峰小时内最大15分钟刷卡量
max_15_count = fifteen_counts.max()
# 根据题目给出的公式计算 PHF5
# PHF5 = 高峰小时刷卡量 ÷ (12 × 高峰小时内最大5分钟刷卡量)
# 因为1小时中有12个5分钟窗口，所以乘以12
PHF5 = peak_count / (12 * max_5_count)
# 根据题目给出的公式计算 PHF15
# PHF15 = 高峰小时刷卡量 ÷ (4 × 高峰小时内最大15分钟刷卡量)
# 因为1小时中有4个15分钟窗口，所以乘以4
PHF15 = peak_count / (4 * max_15_count)
# 设置高峰小时的开始时间，例如 peak_hour=8，则显示为08:00
peak_start = f"{peak_hour:02d}:00"
# 设置高峰小时的结束时间，例如 peak_hour=8，则显示为09:00
peak_end = f"{peak_hour + 1:02d}:00"
# 将最大5分钟窗口的开始时间转成“小时:分钟”格式
five_start = max_5_time.strftime("%H:%M")
# 最大5分钟窗口的结束时间 = 开始时间 + 5分钟
five_end = (max_5_time + pd.Timedelta(minutes=5)).strftime("%H:%M")
# 将最大15分钟窗口的开始时间转成“小时:分钟”格式
fifteen_start = max_15_time.strftime("%H:%M")
# 最大15分钟窗口的结束时间 = 开始时间 + 15分钟
fifteen_end = (max_15_time + pd.Timedelta(minutes=15)).strftime("%H:%M")
# 按题目要求的格式输出高峰小时及PHF结果
print(f"高峰小时：{peak_start} ~ {peak_end}，刷卡量：{peak_count} 次")
print(f"最大5分钟刷卡量（{five_start}~{five_end}）：{max_5_count} 次 PHF5 = {peak_count} / (12 × {max_5_count}) = {PHF5:.4f}")
print(f"最大15分钟刷卡量（{fifteen_start}~{fifteen_end}）：{max_15_count} 次 PHF15 = {peak_count} / (4 × {max_15_count}) = {PHF15:.4f}")
print("\n[任务5]已生成20个文件，路径如下：")


# 导入os库，用于创建文件夹和处理文件路径
import os
# 创建名为“线路驾驶员信息”的文件夹
# exist_ok=True表示如果文件夹已经存在，不会报错
os.makedirs("线路驾驶员信息", exist_ok=True)
# 筛选线路号在1101到1120之间的记录
# 题目要求一共处理这20条线路
routes = df[(df['线路号'] >= 1101) & (df['线路号'] <= 1120)]

# 遍历筛选后数据中实际出现过的每一条线路号
for r in routes['线路号'].unique():

    # 取出当前线路r对应的所有刷卡记录
    temp = routes[routes['线路号'] == r]

    # 提取“车辆编号”和“驾驶员编号”两列
    # drop_duplicates用于去重，避免同一车辆-驾驶员组合重复写入文件
    pairs = temp[['车辆编号', '驾驶员编号']].drop_duplicates()

    # 以线路号作为文件名，例如1101.txt
    # 文件统一保存在“线路驾驶员信息”文件夹中
    with open(f"线路驾驶员信息/{r}.txt", "w", encoding='utf-8') as f:
        f.write(f"线路号: {r}\n")

        # 遍历当前线路下所有去重后的车辆-驾驶员对应关系
        for _, row in pairs.iterrows():
            f.write(f"{row['车辆编号']} {row['驾驶员编号']}\n")

    # 每生成一个文件，就打印该文件路径
    print(f"线路驾驶员信息\\{r}.txt")

# 任务6 服务绩效排名与热力图
# 只保留刷卡类型为0的上车刷卡记录
# 因为题目要求有效刷卡记录代表一次乘客上车
df0 = df[df['刷卡类型'] == 0].copy()
# 统计服务人次最多的Top10司机
# value_counts会统计每个驾驶员编号出现的次数
top_driver = df0['驾驶员编号'].value_counts().head(10)
# 统计服务人次最多的Top10线路
top_route = df0['线路号'].value_counts().head(10)
# 统计服务人次最多的Top10上车站点
top_station = df0['上车站点'].value_counts().head(10)
# 统计服务人次最多的Top10车辆
top_vehicle = df0['车辆编号'].value_counts().head(10)
# 定义一个打印Top10结果的函数，避免重复写相同的打印代码
def print_top10(title, series):
    # 打印每个维度的标题，例如Drivers Top 10
    print(f"\n===== {title} Top 10 =====")
    # enumerate从1开始编号，便于输出Top1到Top10
    for i, (name, count) in enumerate(series.items(), start=1):

        # 打印当前排名、实体编号和对应服务人次
        print(f"Top{i}: {name}  Count={count}")
# 打印司机Top10排名
print_top10("Drivers", top_driver)
# 打印线路Top10排名
print_top10("Routes", top_route)
# 打印上车站点Top10排名
print_top10("Boarding Stations", top_station)
# 打印车辆Top10排名
print_top10("Vehicles", top_vehicle)
# 构造热力图数据矩阵
# 每一行对应一个维度，每一列对应Top1到Top10
heatmap_data = pd.DataFrame(
    [
        top_driver.values,   # Driver行：Top10司机服务人次
        top_route.values,    # Route行：Top10线路服务人次
        top_station.values,  # Boarding Station行：Top10站点服务人次
        top_vehicle.values   # Vehicle行：Top10车辆服务人次
    ],
    index=["Driver", "Route", "Boarding Station", "Vehicle"],
    columns=[f"Top{i}" for i in range(1, 11)]
)
# 创建热力图画布
plt.figure(figsize=(12, 5))
# 使用seaborn绘制热力图
# annot=True表示在每个格子中标注具体数值
# cmap="YlOrRd"表示颜色由浅黄到红色渐变，数值越大颜色越深
sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".0f",
    cmap="YlOrRd"
)
# 设置主标题和副标题
plt.title(
    "Service Performance Ranking Heatmap\n"
    "\n"
    "Counts of valid boarding records (card type = 0)",
    fontsize=14
)
# x轴不额外设置标签
plt.xlabel("")
# y轴不额外设置标签
plt.ylabel("")
# 设置x轴标签水平显示
plt.xticks(rotation=0)
# 保存热力图到当前目录
plt.savefig("performance_heatmap.png", dpi=150, bbox_inches="tight")
# 展示热力图
plt.show()
print("\n【任务6】已保存图像：performance_heatmap.png")
print("\n【任务6】结论说明：")
print(
    "从热力图可以看出，各维度Top1实体的服务人次明显高于同维度其他排名，"
    "说明公交客流在司机、线路、站点和车辆之间存在一定集中性。"
    "其中车辆维度Top1数值最高，表明个别车辆承担了较多运营任务；"
    "上车站点Top10整体数值较高，说明部分站点是客流集散的核心区域。"
)
