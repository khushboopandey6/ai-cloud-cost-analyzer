def generate_insights(cost_data):
    insights = []

    if not cost_data:
        return ["No cost data available"]

    total = sum(cost_data)
    avg = total / len(cost_data)
    max_val = max(cost_data)
    min_val = min(cost_data)

    # trend analysis
    if cost_data[-1] > cost_data[0]:
        insights.append("📈 Your AWS cost is increasing over time")
    else:
        insights.append("📉 Your AWS cost is stable or decreasing")

    # spike detection (realistic threshold)
    if max_val > avg * 1.3:
        insights.append("⚠️ Unusual cost spike detected in usage")

    # cost level check
    if avg > 20:
        insights.append("💡 Consider optimizing EC2 or storage usage")

    if total > 100:
        insights.append("💰 Overall AWS spending is moderate/high")

    if min_val < 10:
        insights.append("🟢 Some services are highly cost efficient")

    return insights
