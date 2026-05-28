import os
import pandas as pd
from src.mock_data import get_mock_cost_data

USE_MOCK = True  # change to False when AWS is ready

def get_cost_data():
    if USE_MOCK:
        return get_mock_cost_data()
    
    # REAL AWS CODE (we will enable later)
    import boto3
    from datetime import datetime, timedelta

    client = boto3.client('ce', region_name='us-east-1')

    today = datetime.today()
    start = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    end = today.strftime('%Y-%m-%d')

    response = client.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    return response


def process_data(data):
    df = pd.DataFrame(data)
    return df
