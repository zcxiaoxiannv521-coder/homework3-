# 张春-25361179-第三次人工智能编程作业

仓库链接：https://github.com/zcxiaoxiannv521-coder/homework3-

---

## 1. 任务拆解与 AI 协作策略

本次作业包含数据清洗、客流统计、线路分析、PHF计算、文件输出以及热力图可视化六个任务。为了保证代码能够正确运行并符合实验要求，我采用了“分任务逐步开发”的方式与AI协作，而不是一次性生成全部代码。

具体流程如下：

### （1）数据读取与清洗

首先让AI帮助完成CSV文件读取、时间字段转换以及ride_stops字段构造。

重点包括：

* 使用pandas读取ICData.csv
* 将“交易时间”转换为datetime格式
* 提取hour字段
* 构造ride_stops = |下车站点 - 上车站点|
* 删除ride_stops=0的异常记录
* 检查并处理缺失值

### （2）任务2：客流统计与可视化

在完成数据清洗后，让AI协助完成：

* 统计早上7点前刷卡量
* 统计晚上22点后刷卡量
* 计算其占全天比例
* 绘制24小时客流分布柱状图
* 对早峰前和深夜时段进行颜色高亮

### （3）任务3：线路平均乘坐站点分析

该部分最初由AI生成基础统计代码，随后经过多次调整：

* 按线路统计平均乘坐站点数
* 计算标准差
* 提取Top15线路
* 绘制横向柱状图
* 添加误差线
* 调整颜色渐变
* 修正线路排序方式

### （4）任务4：PHF高峰小时系数计算

本部分由我与AI共同完成。

主要步骤：

* 找出客流最高小时
* 按5分钟聚合
* 按15分钟聚合
* 计算PHF5
* 计算PHF15
* 调整输出格式使其符合实验要求

### （5）任务5：线路驾驶员文件生成

让AI帮助完成：

* 自动创建文件夹
* 筛选1101~1120线路
* 提取车辆与驾驶员对应关系
* 自动生成20个txt文件

### （6）任务6：服务绩效热力图

先统计：

* Top10司机
* Top10线路
* Top10站点
* Top10车辆

然后使用Seaborn绘制热力图，并补充文字结论分析。

整个过程中采用“生成—运行—调试—优化”的协作方式完成作业。

---

## 2. 核心 Prompt 迭代记录

### 初代 Prompt

请帮我统计各线路平均乘坐站点数，并绘制Top15线路柱状图。

### AI生成的问题

第一次生成的代码存在以下问题：

1. 使用纵向柱状图，不符合参考图要求；
2. 未添加标准差误差线；
3. 颜色顺序与要求不一致；
4. 路线排序方式错误；
5. 图形样式与实验参考图差异较大。

### 优化后的 Prompt

请按照以下要求重新生成：

* 绘制Top15线路横向柱状图；
* 使用Blues配色；
* 添加标准差误差线；
* 横坐标为平均乘坐站点数；
* 纵坐标为线路号；
* 图形样式尽量与实验参考图一致；
* 使用Seaborn绘图。

### 改进效果

经过Prompt优化后：

* 图形方向正确；
* 误差线显示正常；
* 颜色渐变符合要求；
* 排序方式正确；
* 最终图像与实验要求基本一致。

---

## 3. Debug记录

### 报错现象

在绘制任务3图像时程序报错：

ValueError: Could not interpret value 'mean_ride_stops' for y

### 原因分析

DataFrame中实际列名为：

* mean_stops
* std_stops

而绘图代码中错误写成：

mean_ride_stops

导致Seaborn无法找到对应字段。

### 解决过程

首先打印DataFrame列名：

```python
print(top15.columns)
```

发现实际字段名称为：

```python
Index(['线路号','mean_stops','std_stops'])
```

随后修改绘图代码：

```python
x='mean_stops'
```

替换错误字段：

```python
x='mean_ride_stops'
```

程序重新运行后成功生成图像。

### 调试收获

在使用AI生成代码时，不能直接复制运行，需要检查：

* DataFrame字段名称
* 分组统计结果
* 排序结果
* 绘图参数

通过打印中间变量能够快速定位问题。

---

## 4. 人工代码审查（逐行中文注释）

下面以任务4 PHF计算为例进行人工代码审查。

```python
# 只保留刷卡类型为0的数据
df0 = df[df['刷卡类型'] == 0].copy()

# 按小时统计刷卡量
hour_counts = df0.groupby('hour').size()

# 找到刷卡量最大的小时
peak_hour = hour_counts.idxmax()

# 获取该小时刷卡总量
peak_count = hour_counts.max()

# 提取高峰小时内的数据
peak_df = df0[df0['hour'] == peak_hour].copy()

# 将时间向下取整到5分钟粒度
peak_df['time_5min'] = peak_df['交易时间'].dt.floor('5min')

# 统计每个5分钟区间的刷卡量
five_counts = peak_df.groupby('time_5min').size()

# 找出刷卡量最大的5分钟区间
max_5_time = five_counts.idxmax()

# 获取该区间刷卡量
max_5_count = five_counts.max()

# 将时间向下取整到15分钟粒度
peak_df['time_15min'] = peak_df['交易时间'].dt.floor('15min')

# 统计每个15分钟区间刷卡量
fifteen_counts = peak_df.groupby('time_15min').size()

# 找出刷卡量最大的15分钟区间
max_15_time = fifteen_counts.idxmax()

# 获取该区间刷卡量
max_15_count = fifteen_counts.max()

# 计算PHF5
PHF5 = peak_count / (12 * max_5_count)

# 计算PHF15
PHF15 = peak_count / (4 * max_15_count)
```

### 理解说明

PHF（Peak Hour Factor）用于衡量高峰小时内客流分布是否均匀。

PHF5公式：

PHF5 = 高峰小时总客流 ÷ （12 × 最大5分钟客流）

PHF15公式：

PHF15 = 高峰小时总客流 ÷ （4 × 最大15分钟客流）

PHF越接近1，说明高峰小时内部客流越均匀；越接近0，则说明客流集中在少数时间段内。
