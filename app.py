import streamlit as st
import matplotlib.pyplot as plt

from src.data_cleaning import DataCleaner
from src.kpi_engine import KPIEngine
from src.drop_detection import DropDetector
from src.root_cause import RootCauseAnalyzer
from src.impact_analysis import ImpactAnalyzer
from src.recommendation_engine import RecommendationEngine

st.set_page_config(page_title="KPI Drop Analysis Dashboard", layout="wide")

st.title("📊 Superstore KPI Drop Analysis Dashboard")

# =============================
# LOAD & CLEAN DATA
# =============================
cleaner = DataCleaner("data/train.csv")
cleaner.load_data()
df = cleaner.clean_data()

# =============================
# KPI CALCULATION
# =============================
kpi_engine = KPIEngine(df)
kpis = kpi_engine.calculate_monthly_kpis()

# =============================
# KPI DASHBOARD
# =============================
st.subheader("📈 KPI Trends")

fig, axes = plt.subplots(2, 2, figsize=(14, 8))

axes[0,0].plot(kpis["year_month"], kpis["sales"])
axes[0,0].set_title("Total Sales Trend")
axes[0,0].tick_params(axis='x', rotation=45)

axes[0,1].plot(kpis["year_month"], kpis["profit"])
axes[0,1].set_title("Total Profit Trend")
axes[0,1].tick_params(axis='x', rotation=45)

axes[1,0].plot(kpis["year_month"], kpis["profit_margin_%"])
axes[1,0].set_title("Profit Margin Trend")
axes[1,0].tick_params(axis='x', rotation=45)

axes[1,1].plot(kpis["year_month"], kpis["sales_growth_%"])
axes[1,1].set_title("Sales Growth %")
axes[1,1].tick_params(axis='x', rotation=45)

plt.tight_layout()
st.pyplot(fig)

# =============================
# DROP DETECTION
# =============================
detector = DropDetector(kpis)
drops = detector.detect_drops()

st.subheader("🚨 KPI Drop Detection")

if drops.empty:
    st.success("No significant KPI drop detected.")
else:
    st.error("KPI Drop Detected!")
    st.dataframe(drops)

    problem_month = drops.iloc[0]["year_month"]

    # =============================
    # ROOT CAUSE
    # =============================
    st.subheader("🔎 Root Cause Analysis")

    root = RootCauseAnalyzer(df)

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Region Impact")
        st.dataframe(root.analyze_region(problem_month))

    with col2:
        st.write("### Category Impact")
        st.dataframe(root.analyze_category(problem_month))

# =============================
# BUSINESS IMPACT
# =============================
st.subheader("💰 Business Impact")

impact = ImpactAnalyzer(kpis).calculate_impact()
st.write(impact)

# =============================
# RECOMMENDATIONS
# =============================
st.subheader("📌 Recommendations")

for r in RecommendationEngine().generate(impact):
    st.write("- ", r)
