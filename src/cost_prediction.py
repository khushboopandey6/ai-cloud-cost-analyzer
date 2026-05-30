import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_next_month_cost(cost_history):
    """
    cost_history: list of monthly costs like [120, 150, 170, 200]
    """

    X = np.array(range(len(cost_history))).reshape(-1, 1)
    y = np.array(cost_history)

    model = LinearRegression()
    model.fit(X, y)

    next_month = len(cost_history)
    prediction = model.predict([[next_month]])

    return round(float(prediction[0]), 2)
