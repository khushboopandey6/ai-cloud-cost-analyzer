import os
from groq import Groq


def generate_chat_response(question, cost_history, df):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "AI chat unavailable — GROQ_API_KEY not set."

    total = sum(cost_history)
    service_summary = df.groupby("service")["cost"].sum().round(2).to_dict()

    system_prompt = f"""You are an AWS cost optimization assistant. You have access to the following real cost data:

Monthly costs (oldest to newest, USD): {cost_history}
Total spend tracked: ${total:.2f}
Monthly average: ${total / len(cost_history):.2f}
Cost by service: {service_summary}

Answer the user's question about their AWS costs clearly and helpfully.
Give specific, actionable advice using the actual numbers above.
Keep responses concise — 2 to 4 sentences max."""

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI error: {str(e)}"
