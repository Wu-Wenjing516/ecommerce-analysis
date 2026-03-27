# 电商多平台价格与品类利润数据分析项目

## 项目背景
本项目基于阿里云天池实验室电商业务真实数据集（may-2022商品数据表），通过Python实现数据读取、清洗、多维度分析与可视化，挖掘品类结构、多平台定价差异、成本利润等核心业务信息，为库存备货、渠道运营、定价策略与营销推广提供数据支撑与决策依据。

## 技术栈
- 编程语言：Python
- 数据处理：Pandas
- 数据可视化：Matplotlib
- 数据库：MySQL
- 数据库连接：SQLAlchemy、PyMySQL

## 数据集说明
数据表：`may-2022`
包含字段：
- 商品基础信息：Sku、Style Id、Catalog、Category、Weight
- 成本价格：TP（拿货成本价）
- 多平台售价：Amazon MRP、Flipkart MRP、Myntra MRP、Ajio MRP、Limeroad MRP、Paytm MRP、Snapdeal MRP、Amazon FBA MRP
- 历史价格：MRP Old、Final MRP Old

## 分析维度
1. 商品品类结构与分布分析
2. 多平台售价对比与定价策略分析
3. 成本价、售价、利润与利润率分析
4. 高利润品类挖掘与排行
5. 商品价格区间分布分析
6. 利润分布与盈利水平评估

## 可视化图表
1. TOP10商品品类数量柱状图
2. 各电商平台平均售价对比图
3. 成本价与售价分布直方图
4. TOP10品类平均利润柱状图
5. 商品价格区间占比饼图
6. 单品利润分布直方图
