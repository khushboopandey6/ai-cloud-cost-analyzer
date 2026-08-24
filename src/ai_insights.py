import os
from groq import Groq


def generate_insights(cost_data):
    try:
        return _groq_insights(cost_data)
    except Exception:
        return _rule_based_insights(cost_data)


def _groq_insights(cost_data):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or not cost_data:
        raise ValueError("missing key or data")

    total = sum(cost_data)
    avg = total / len(cost_data)
    growth = ((cost_data[-1] - cost_data[0]) / cost_data[0]) * 100 if cost_data[0] != 0 else 0
    trend = "increasing" if cost_data[-1] > cost_data[0] else "stable or decreasing"

    prompt = f"""You are an AWS cost optimization expert. Analyze this cloud cost data and give 4-5 short, specific, actionable insights.

Monthly AWS costs (oldest to newest, in USD): {cost_data}
Total spend tracked: ${total:.2f}
Monthly average: ${avg:.2f}
Overall trend: {trend}
Growth over period: {growth:.1f}%

Rules:
- Each insight must be 1-2 sentences max
- Use actual numbers from the data
- Include specific, actionable recommendations
- Start each insight with a relevant emoji
- Return plain text, one insight per line, no bullet points or numbering"""

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.choices[0].message.content
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    if not lines:
        raise ValueError("empty response")
    return lines


def _rule_based_insights(cost_data):
    if not cost_data:
        return ["No cost data available"]

    insights = []
    total = sum(cost_data)
    avg = total / len(cost_data)
    max_val = max(cost_data)

    if cost_data[-1] > cost_data[0]:
        insights.append("📈 Your AWS cost is increasing over time")
    else:
        insights.append("📉 Your AWS cost is stable or decreasing")

    if cost_data[0] != 0:
        growth = (cost_data[-1] - cost_data[0]) / cost_data[0] * 100
        if growth > 50:
            insights.append(f"🚨 Costs have grown {growth:.0f}% over the tracked period — review your resource usage")

    if max_val > avg * 1.3:
        insights.append("⚠️ Unusual cost spike detected in one or more months")

    if avg > 200:
        insights.append("💡 Monthly average exceeds $200 — consider Reserved Instances or Savings Plans")

    if total > 2000:
        insights.append(f"💰 Total tracked spend is ${total:.0f} — review reserved pricing options")

    return insights
