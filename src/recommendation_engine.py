class RecommendationEngine:

    def generate(self, impact):

        # If impact is a string (not enough data case)
        if isinstance(impact, str):
            return ["Not enough data to generate recommendations."]

        recommendations = []

        sales_loss = impact.get("Average Sales Loss", 0)
        profit_loss = impact.get("Average Profit Loss", 0)

        if sales_loss > 0:
            recommendations.append(
                "Investigate decline in sales. Consider promotions or targeted marketing campaigns."
            )

        if profit_loss > 0:
            recommendations.append(
                "Profit margins are shrinking. Review discount strategy and supplier costs."
            )

        if sales_loss <= 0 and profit_loss <= 0:
            recommendations.append(
                "KPIs are stable. Continue monitoring performance."
            )

        return recommendations
