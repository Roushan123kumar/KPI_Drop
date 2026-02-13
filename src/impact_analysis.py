class ImpactAnalyzer:

    def __init__(self, kpis):
        self.kpis = kpis

    def calculate_impact(self):

        # Take last 2 months vs previous 2 months
        recent = self.kpis.tail(2)
        previous = self.kpis.iloc[-4:-2]

        if previous.empty or recent.empty:
            return "Not enough data to calculate impact."

        sales_loss = previous["sales"].mean() - recent["sales"].mean()
        profit_loss = previous["profit"].mean() - recent["profit"].mean()

        return {
            "Average Sales Loss": round(sales_loss, 2),
            "Average Profit Loss": round(profit_loss, 2)
        }
