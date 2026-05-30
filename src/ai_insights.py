def generate_insights(cost_data):
    insights = []

    total = sum(cost_data)

    if total > 200:
        insights.append("⚠️ Your AWS cost is high. Consider optimizing EC2 usage.")

    if cost_data[-1] > cost_data[-2]:
        insights.append("📈 Cost is increasing month-over-month.")

    if max(cost_data) > 100:
        insights.append("💡 High spike detected in AWS usage.")

    return insights
