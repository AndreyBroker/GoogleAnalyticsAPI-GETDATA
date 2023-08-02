from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest
)
from google.oauth2 import service_account
import os
import pandas as pd

PROP_ID = os.environ['PROP_ID']
SECRET_KEY = os.environ['KEY_PATH']

credentials = service_account.Credentials.from_service_account_file(SECRET_KEY)
client = BetaAnalyticsDataClient(credentials=credentials)

request = RunReportRequest(

    property=f"properties/{PROP_ID}",
    dimensions=[Dimension(name='date')],
    metrics=[Metric(name='customUser:businnes_size')],
    date_ranges=[DateRange(start_date="7daysAgo", end_date="today")]

)

response = client.run_report(request)

def ga4_result_to_df(response):
    """Original: print_run_report_response: Prints results of a runReport call. v2.1 changed by Bram to create DataFrame"""
    result_dict = {}  
    for dimensionHeader in response.dimension_headers:
        result_dict[dimensionHeader.name] = []
    for metricHeader in response.metric_headers:
        result_dict[metricHeader.name] = []
    for rowIdx, row in enumerate(response.rows):
        for i, dimension_value in enumerate(row.dimension_values):
            dimension_name = response.dimension_headers[i].name
            result_dict[dimension_name].append(dimension_value.value)
        for i, metric_value in enumerate(row.metric_values):
            metric_name = response.metric_headers[i].name
            result_dict[metric_name].append(metric_value.value)
    return pd.DataFrame(result_dict)

print(ga4_result_to_df(response))