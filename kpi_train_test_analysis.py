import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12,6)

# =====================================================
# 1️⃣ LOAD DATA
# =====================================================
df = pd.read_csv("data/train.csv")

# =====================================================
# 2️⃣ CLEAN COLUMN NAMES
# =====================================================
df = df.loc[:, ~df.columns.duplicated()]
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# =====================================================
# 3️⃣ DATA TYPE CONVERSION
# =====================================================
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df['ship_date'] = pd.to_datetime(df['ship_date'], errors='coerce')
df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
df['profit'] = pd.to_numeric(df['profit'], errors='coerce')
df['postal_code'] = df['postal_code'].astype(str)

df.dropna(subset=['order_date', 'ship_date', 'sales', 'profit'], inplace=True)

# =====================================================
# 4️⃣ FEATURE ENGINEERING
# =====================================================
df['year_month'] = df['order_date'].dt.to_period('M')
df['shipping_days'] = (df['ship_date'] - df['order_date']).dt.days

df = df[df['shipping_days'] >= 0]
df = df[df['sales'] <= df['sales'].quantile(0.99)]

# =====================================================
# 5️⃣ SORT BY TIME (CRITICAL)
# =====================================================
df = df.sort_values(by='order_date').reset_index(drop=True)

# =====================================================
# 6️⃣ TRAIN / TEST SPLIT (70% / 30%)
# =====================================================
split_index = int(len(df) * 0.7)

train_df = df.iloc[:split_index]
test_df = df.iloc[split_index:]

print("Train Size:", train_df.shape)
print("Test Size:", test_df.shape)

print("Train Period:", train_df['order_date'].min().date(),
      "to", train_df['order_date'].max().date())
print("Test Period:", test_df['order_date'].min().date(),
      "to", test_df['order_date'].max().date())

# =====================================================
# 7️⃣ KPI CALCULATION (TRAIN)
# =====================================================
train_kpi = (
    train_df.groupby('year_month')
    .agg({'sales':'sum', 'profit':'sum'})
    .reset_index()
)

train_kpi['year_month'] = train_kpi['year_month'].astype(str)
train_kpi['profit_margin_%'] = (train_kpi['profit'] / train_kpi['sales']) * 100
train_kpi['sales_growth_%'] = train_kpi['sales'].pct_change() * 100

# =====================================================
# 8️⃣ KPI CALCULATION (TEST)
# =====================================================
test_kpi = (
    test_df.groupby('year_month')
    .agg({'sales':'sum', 'profit':'sum'})
    .reset_index()
)

test_kpi['year_month'] = test_kpi['year_month'].astype(str)
test_kpi['profit_margin_%'] = (test_kpi['profit'] / test_kpi['sales']) * 100
test_kpi['sales_growth_%'] = test_kpi['sales'].pct_change() * 100

# =====================================================
# 9️⃣ KPI DROP DETECTION (TEST DATA)
# =====================================================
drop_months = test_kpi[test_kpi['sales_growth_%'] < -10]

print("\n🔻 KPI Drops in TEST Period:")
print(drop_months)

# =====================================================
# 🔟 KPI TREND GRAPH (TRAIN vs TEST)
# =====================================================
plt.figure(figsize=(12,5))
plt.plot(train_kpi['year_month'], train_kpi['sales'], label='Train (70%)', marker='o')
plt.plot(test_kpi['year_month'], test_kpi['sales'], label='Test (30%)', marker='o')
plt.xticks(rotation=90)
plt.title("Monthly Sales – Train vs Test")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.legend()
plt.tight_layout()
plt.show()

# =====================================================
# 1️⃣1️⃣ ROOT CAUSE ANALYSIS (IF DROP FOUND)
# =====================================================
if not drop_months.empty:
    drop_period = drop_months.iloc[0]['year_month']
    prev_period = str(pd.Period(drop_period) - 1)

    curr = test_df[test_df['year_month'].astype(str) == drop_period]
    prev = test_df[test_df['year_month'].astype(str) == prev_period]

    print("\n📌 Root Cause Analysis for:", drop_period)

    region_change = curr.groupby('region')['sales'].sum() - prev.groupby('region')['sales'].sum()
    category_change = curr.groupby('category')['sales'].sum() - prev.groupby('category')['sales'].sum()
    segment_change = curr.groupby('segment')['sales'].sum() - prev.groupby('segment')['sales'].sum()

    print("\nRegion Impact:")
    print(region_change)

    print("\nCategory Impact:")
    print(category_change)

    print("\nSegment Impact:")
    print(segment_change)

    # =================================================
    # 1️⃣2️⃣ ROOT CAUSE GRAPHS
    # =================================================
    fig, axes = plt.subplots(1, 3, figsize=(18,5))

    region_change.plot(kind='bar', ax=axes[0], title="Region Impact")
    category_change.plot(kind='bar', ax=axes[1], title="Category Impact", color='orange')
    segment_change.plot(kind='bar', ax=axes[2], title="Segment Impact", color='green')

    plt.tight_layout()
    plt.show()

    # =================================================
    # 1️⃣3️⃣ BUSINESS IMPACT
    # =================================================
    sales_loss = (
        test_kpi.loc[test_kpi['year_month'] == drop_period, 'sales'].values[0]
        - test_kpi.loc[test_kpi['year_month'] == prev_period, 'sales'].values[0]
    )

    print("\n💰 Estimated Revenue Impact:", abs(round(sales_loss,2)))

    # =================================================
    # 1️⃣4️⃣ RECOMMENDATIONS
    # =================================================
    print("\n📌 BUSINESS RECOMMENDATIONS:")

    if region_change.min() < 0:
        print(f"- Focus recovery strategy in {region_change.idxmin()} region")

    if category_change.min() < 0:
        print(f"- Review pricing and promotion for {category_change.idxmin()} category")

    if segment_change.min() < 0:
        print(f"- Target retention offers for {segment_change.idxmin()} customers")

# =====================================================
# 1️⃣5️⃣ FINAL MESSAGE
# =====================================================
print("""
✅ ANALYSIS COMPLETE

• Time-based 70% / 30% split
• KPI trained on historical data
• Drop detected on future data
• Root cause identified
• Business impact calculated
• Actionable recommendations generated
""")
