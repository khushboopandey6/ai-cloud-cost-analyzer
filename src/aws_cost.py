import boto3
import pandas as pd
from datetime import datetime
from src.mock_data import get_mock_cost_data


def get_cost_data():
    client = boto3.client('ce', region_name='us-east-1')

    end = datetime.today().strftime('%Y-%m-%d')
    start = (pd.Timestamp.today() - pd.DateOffset(months=12)).strftime('%Y-%m-%d')

    response = client.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    return response


def process_data(response):
    rows = []
    for period in response['ResultsByTime']:
        month = period['TimePeriod']['Start'][:7]
        for group in period['Groups']:
            service = group['Keys'][0]
            cost = float(group['Metrics']['UnblendedCost']['Amount'])
            if cost > 0:
                rows.append({'month': month, 'service': service, 'cost': cost})

    df = pd.DataFrame(rows) if rows else pd.DataFrame(columns=['month', 'service', 'cost'])

    # Fall back to demo data when real AWS costs are negligible
    if df.empty or df['cost'].sum() < 1.0:
        return pd.DataFrame(get_mock_cost_data())

    return df


def get_monthly_totals(df):
    monthly = df.groupby('month')['cost'].sum().sort_index()
    return monthly.tolist()
