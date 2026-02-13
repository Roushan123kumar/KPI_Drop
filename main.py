from src.data_cleaning import DataCleaner
import matplotlib.pyplot as plt
from src.kpi_engine import KPIEngine
from src.drop_detection import DropDetector
from src.root_cause import RootCauseAnalyzer
from src.impact_analysis import ImpactAnalyzer
from src.recommendation_engine import RecommendationEngine


def main():

    # Step 1: Clean Data
    cleaner = DataCleaner("data/train.csv")
    cleaner.load_data()
    df = cleaner.clean_data()

    # Step 2: KPI Engine
    kpi_engine = KPIEngine(df)
    kpis = kpi_engine.calculate_monthly_kpis()
        # ===============================
    # KPI DASHBOARD
    # ===============================
    fig, axes = plt.subplots(2, 2, figsize=(14,10))

    # Sales Trend
    axes[0,0].plot(kpis["Month"], kpis["Sales"])
    axes[0,0].set_title("Total Sales Trend")
    axes[0,0].tick_params(axis='x', rotation=45)

    # Profit Trend
    axes[0,1].plot(kpis["Month"], kpis["Profit"], color='green')
    axes[0,1].set_title("Total Profit Trend")
    axes[0,1].tick_params(axis='x', rotation=45)

    # Profit Margin
    axes[1,0].plot(kpis["Month"], kpis["Profit_Margin_%"], color='purple')
    axes[1,0].set_title("Profit Margin Trend")
    axes[1,0].tick_params(axis='x', rotation=45)

    # Sales Growth
    axes[1,1].plot(kpis["Month"], kpis["Sales_Growth_%"], color='orange')
    axes[1,1].set_title("Sales Growth %")
    axes[1,1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig("kpi_dashboard.png", dpi=300)
    plt.show()


    # Step 3: Detect Drops
    detector = DropDetector(kpis)
    drops = detector.detect_drops()

    print("\nKPI Drops Detected:")
    print(drops)

    # Step 4: Root Cause
    if not drops.empty:
        problem_month = drops.iloc[0]["Month"]

        root = RootCauseAnalyzer(df)
        print("\nRegion Analysis:")
        print(root.analyze_region(problem_month))

        print("\nCategory Analysis:")
        print(root.analyze_category(problem_month))

    # Step 5: Impact
    impact_analyzer = ImpactAnalyzer(kpis)
    impact = impact_analyzer.calculate_impact()

    print("\nBusiness Impact:")
    print(impact)

    # Step 6: Recommendations
    rec_engine = RecommendationEngine()
    recommendations = rec_engine.generate(impact)

    print("\nRecommendations:")
    for r in recommendations:
        print("-", r)


if __name__ == "__main__":
    main()
