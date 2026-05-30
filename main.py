from fastapi import FastAPI
from src.aws_cost import get_cost_data, process_data
from src.cost_prediction import predict_next_month_cost
from src.ai_insights import generate_insights

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running 🚀"}

# =========================
# 💰 COST API
# =========================
@app.get("/cost")
def get_cost():
    response = get_cost_data()
    df = process_data(response)

    return {
        "total_cost": float(df["cost"].sum()),
        "data": df.to_dict(orient="records")
    }

# =========================
# 🤖 AI ANALYSIS API
# =========================
@app.get("/ai-analysis")
def ai_analysis():
    response = get_cost_data()
    df = process_data(response)

    cost_history = df["cost"].tolist()

    if len(cost_history) < 2:
        return {
            "error": "Not enough data for AI analysis"
        }

    predicted_cost = predict_next_month_cost(cost_history)
    insights = generate_insights(cost_history)

    return {
        "current_month_costs": cost_history,
        "predicted_next_month_cost": predicted_cost,
        "insights": insights
    }
