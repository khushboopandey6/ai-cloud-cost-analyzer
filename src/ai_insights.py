def generate_insights(cost_history):
    insights = []

    if len(cost_history) < 2:
        return ["Not enough data for insights"]

    avg_cost = sum(cost_history) / len(cost_history)
    max_cost = max(cost_history)
    min_cost = min(cost_history)

    # trend detection
    if cost_history[-1] > cost_history[0]:
        insights.append("📈 Your AWS cost is increasing over time")
    else:
        insights.append("📉 Your AWS cost is stable or decreasing")

    # spike detection
    if max_cost > avg_cost * 1.5:
        insights.append("⚠️ High cost spike detected in usage")

    # optimization hint
    if avg_cost > 20:
        insights.append("💡 Consider optimizing EC2 or storage usage")

    # low cost note
    if min_cost < 10:
        insights.append("🟢 Some services are highly cost efficient")

    return insights
