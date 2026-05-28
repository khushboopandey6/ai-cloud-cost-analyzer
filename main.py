from fastapi import FastAPI
from src.aws_cost import get_cost_data, process_data

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running 🚀"}

@app.get("/cost")
def get_cost():
    response = get_cost_data()
    df = process_data(response)

    return {
        "total_cost": float(df["cost"].sum()),
        "data": df.to_dict(orient="records")
    }
