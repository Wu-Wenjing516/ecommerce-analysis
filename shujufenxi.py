# ==========================
# 豪雅集团数据分析岗项目实战代码
# 项目：电商销售数据可视化与分析报告
# 技术栈：Python, Pandas, Matplotlib, MySQL
# ==========================

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# ----------------------
# 1. 连接 MySQL 读取数据（无警告版本）
# ----------------------
# 格式：mysql+pymysql://用户名:密码@localhost:3306/数据库名?charset=utf8
engine = create_engine("mysql+pymysql://root:Mysql12024!@localhost:3306/ecommerce?charset=utf8")

# 读取你导入的表：may-2022
df = pd.read_sql("SELECT * FROM `may-2022`", engine)
print("✅ 从MySQL读取数据成功，共", len(df), "条数据")
print(df.head())


# ----------------------
# 2. 数据清洗
# ----------------------
def clean_data(df):
    df = df.drop_duplicates()
    df = df.dropna()

    # 清洗 TP 拿货价
    if "TP" in df.columns:
        df["TP"] = pd.to_numeric(df["TP"], errors="coerce")
        df = df[df["TP"].notna()]
        df = df[df["TP"] > 0]

    # 清洗 Myntra MRP 售价
    if "Myntra MRP" in df.columns:
        df["Myntra MRP"] = df["Myntra MRP"].astype(str).str.strip()
        df = df[df["Myntra MRP"] != "Nill"]
        df["Myntra MRP"] = pd.to_numeric(df["Myntra MRP"], errors="coerce")
        df = df[df["Myntra MRP"].notna()]

    # 过滤无效品类
    if "Category" in df.columns:
        df = df[df["Category"] != "Nill"]

    return df

df_clean = clean_data(df)
print("\n✅ 数据清洗完成")

# ----------------------
# 3. 分析
# ----------------------
cate_sales = df_clean["Category"].value_counts().sort_values(ascending=False)
top3_cate = cate_sales.head(3)

df_clean["利润空间"] = df_clean["Myntra MRP"] - df_clean["TP"]

# ----------------------
# 4. 输出结果
# ----------------------
print("\n===== 📊 分析结果 =====")
print("TOP3 核心商品品类：")
print(top3_cate)

print("\n💰 平均拿货价：", round(df_clean["TP"].mean(), 2))
print("💰 平均售价：", round(df_clean["Myntra MRP"].mean(), 2))
print("💰 平均利润空间：", round(df_clean["利润空间"].mean(), 2))

# ----------------------
# 5. 可视化
# ----------------------
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 图1：品类分布
plt.figure(figsize=(10, 4))
top3_cate.plot(kind="bar", color="#1f77b4")
plt.title("TOP3 商品品类数量分布")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# 图2：利润分布
plt.figure(figsize=(10, 4))
df_clean["利润空间"].plot(kind="hist", bins=20, color="#ff7f0e")
plt.title("商品利润空间分布")
plt.tight_layout()
plt.show()

# ----------------------
# 6. 业务报告
# ----------------------
print("\n===== 📝 业务分析报告 =====")
print("1. 核心品类为 Kurta、Kurta Set、Tops，品类集中度高，可重点备货")
print("2. 商品利润空间稳定，盈利性良好")
print("3. 可优先保障TOP3品类库存，加大高利润商品推广")