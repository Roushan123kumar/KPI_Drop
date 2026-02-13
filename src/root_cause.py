class RootCauseAnalyzer:

    def __init__(self, df):
        self.df = df

    def analyze_region(self, problem_month):
        problem_data = self.df[self.df["year_month"] == problem_month]

        return (
            problem_data.groupby("region")
            .agg(
                total_sales=("sales", "sum"),
                total_profit=("profit", "sum")
            )
            .reset_index()
            .sort_values("total_sales")
        )

    def analyze_category(self, problem_month):
        problem_data = self.df[self.df["year_month"] == problem_month]

        return (
            problem_data.groupby("category")
            .agg(
                total_sales=("sales", "sum"),
                total_profit=("profit", "sum")
            )
            .reset_index()
            .sort_values("total_sales")
        )
