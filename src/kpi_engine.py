class KPIEngine:

    def __init__(self, df):
        self.df = df

    def calculate_monthly_kpis(self):

        kpis = (
            self.df.groupby("year_month")
            .agg({
                "sales": "sum",
                "profit": "sum"
            })
            .reset_index()
        )

        kpis["year_month"] = kpis["year_month"].astype(str)
        kpis["profit_margin_%"] = (kpis["profit"] / kpis["sales"]) * 100
        kpis["sales_growth_%"] = kpis["sales"].pct_change() * 100

        return kpis
