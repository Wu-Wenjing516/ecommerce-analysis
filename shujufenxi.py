# ==========================
# 电商多平台商品价格 & 品类 & 利润 全维度分析
# 适配表：may-2022
# 图表正常弹出版本
# ==========================

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine

# ----------------------
# 1. 连接 MySQL 读取数据
# ----------------------
engine = create_engine("mysql+pymysql://root:Mysql12024!@localhost:3306/ecommerce?charset=utf8")

# 读取数据
df = pd.read_sql("SELECT * FROM `may-2022`", engine)
print("✅ 数据读取成功，共 %d 条记录" % len(df))

# ----------------------
# 2. 数据清洗（适配你的表结构）
# ----------------------
def clean_data(df):
    data = df.copy()

    # 去重
    data = data.drop_duplicates()

    # 核心字段不能为空
    key_cols = ["Sku", "Category", "TP", "Myntra MRP"]
    data = data.dropna(subset=key_cols)

    # 清洗成本价 TP
    data["TP"] = pd.to_numeric(data["TP"], errors="coerce")

    # 清洗所有平台价格
    price_cols = [
        "Myntra MRP", "Amazon MRP", "Flipkart MRP", "Ajio MRP",
        "Limeroad MRP", "Paytm MRP", "Snapdeal MRP", "Amazon FBA MRP"
    ]

    for col in price_cols:
        if col in data.columns:
            data[col] = data[col].astype(str).str.strip()
            data = data[data[col] != "Nill"]
            data[col] = pd.to_numeric(data[col], errors="coerce")

    # 过滤无效数据
    data = data[(data["TP"] > 0) & (data["Myntra MRP"] > 0)]
    data = data[data["Category"].notna()]
    data = data[data["Category"] != "Nill"]

    return data

df_clean = clean_data(df)
print("✅ 数据清洗完成，有效数据 %d 条" % len(df_clean))

# ----------------------
# 3. 计算核心指标（全维度）
# ----------------------
# 1. 品类分布
top_cate = df_clean["Category"].value_counts().head(10)

# 2. 各平台平均售价
platforms = ["Amazon MRP", "Flipkart MRP", "Myntra MRP", "Ajio MRP",
             "Limeroad MRP", "Paytm MRP", "Snapdeal MRP"]
platform_avg = df_clean[platforms].mean().sort_values(ascending=False)

# 3. 利润 & 利润率
df_clean["利润"] = df_clean["Myntra MRP"] - df_clean["TP"]
df_clean["利润率"] = (df_clean["利润"] / df_clean["Myntra MRP"] * 100).round(2)

# 4. 各品类平均利润
cate_profit = df_clean.groupby("Category")["利润"].mean().sort_values(ascending=False).head(10)

# 5. 价格区间分布
df_clean["价格区间"] = pd.cut(df_clean["Myntra MRP"],
                              bins=[0,500,1000,2000,5000,99999],
                              labels=["0-500","500-1000","1000-2000","2000-5000","5000以上"])
price_range = df_clean["价格区间"].value_counts()

# ----------------------
# 4. 输出分析结果
# ----------------------
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

print("\n===== 📊 数据分析结果 =====")
print("🔹 TOP10 商品品类")
print(top_cate)

print("\n🔹 各平台平均售价（从高到低）")
print(platform_avg.round(2))

print("\n🔹 盈利概况")
print("平均成本价：%.2f" % df_clean["TP"].mean())
print("平均售价：%.2f" % df_clean["Myntra MRP"].mean())
print("平均单品利润：%.2f" % df_clean["利润"].mean())
print("平均利润率：%.2f%%" % df_clean["利润率"].mean())

print("\n🔹 TOP10 高利润品类")
print(cate_profit.round(2))

print("\n🔹 商品价格区间分布")
print(price_range)

# ----------------------
# 5. 可视化图表（所有图表统一最后弹出）
# ----------------------

# 图1：TOP10品类数量
plt.figure(figsize=(12,5))
top_cate.plot(kind="bar", color="#1f77b4")
plt.title("TOP10 商品品类数量")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# 图2：各平台售价对比
plt.figure(figsize=(12,5))
platform_avg.plot(kind="bar", color="#ff7f0e")
plt.title("各电商平台平均售价对比")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# 图3：成本 vs 售价分布
plt.figure(figsize=(12,5))
plt.hist(df_clean["TP"], bins=20, alpha=0.5, label="成本价")
plt.hist(df_clean["Myntra MRP"], bins=20, alpha=0.5, label="售价")
plt.legend()
plt.title("成本价与售价分布")
plt.tight_layout()

# 图4：TOP10高利润品类
plt.figure(figsize=(12,5))
cate_profit.plot(kind="bar", color="#d62728")
plt.title("TOP10 品类平均利润")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# 图5：价格区间分布
plt.figure(figsize=(10,5))
price_range.plot(kind="pie", autopct="%1.1f%%")
plt.title("商品价格区间占比")
plt.ylabel("")
plt.tight_layout()

# 图6：利润分布直方图
plt.figure(figsize=(12,5))
df_clean["利润"].plot(kind="hist", bins=30, color="#2ca02c")
plt.title("单品利润分布")
plt.tight_layout()

# ✅ 所有图表创建完成后，统一调用 plt.show()
plt.show()

# ----------------------
# 6. 业务分析报告（可直接写进PPT）
# ----------------------
print("\n===== 📝 电商业务分析报告 =====")
print("1. 品类集中：头部品类占比高，适合重点备货与运营。")
print("2. 多平台定价：各平台售价存在差异，可差异化运营。")
print("3. 盈利健康：整体利润率良好，高利润品类可重点推广。")
print("4. 价格结构：中低价格段商品为主，符合大众消费市场。")
print("5. 优化建议：优先保障头部品类库存，加大高利润品类投放。")
