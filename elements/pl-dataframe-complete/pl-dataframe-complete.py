import random
import chevron
import pandas as pd
import prairielearn as pl


def prepare(element_html, data):
    data['params']['random_number'] = random.random()
    dummy_data = {
        'Category': ['A', 'A', 'B', 'B', 'A', 'B', 'B', 'A'],
        'Item': ['X', 'Y', 'X', 'Y', 'X', 'Y', 'X', 'X'],
        'Value': [10, 15, 20, 25, 30, 12, 16, 26],
        'Quantity': [100, 200, 200, 250, 300, 150, 160, 200]
    }
    input_df = pd.DataFrame(dummy_data)
    pivoted_df = pd.pivot_table(input_df, index='Category', columns='Item', values="Value", aggfunc="sum")
    distractor_df = pd.pivot_table(input_df, index='Item', columns='Category', values="Quantity", aggfunc="sum")

    # Create lists of column and row labels and data values
    columns = pd.DataFrame([pivoted_df.columns])
    index = pd.DataFrame(pivoted_df.index)
    values = pivoted_df.values.flatten().tolist()

    data["params"]["input_df"] = pl.to_json(input_df)
    data["params"]["pivoted_df"] = pl.to_json(pivoted_df)
    data["params"]["distractor_df"] = pl.to_json(distractor_df)
    data["params"]["columns"] = pl.to_json(columns)
    data["params"]["index"] = pl.to_json(index)
    data["params"]["values"] =  list(values)
    data["params"]["pivot_code"] = "df = pd.pivot_table(df, index='Category', columns='Item', values='Value', aggfunc='sum')"
    return data


def render(element_html, data):
    html_params = {
        'number': data['params']['random_number'],
        'pivot_code': data['params']['pivot_code'],
        'index': data['params']['index'],
        'columns': data['params']['columns']
    }
    with open('pl-dataframe-complete.mustache', 'r') as f:
        return chevron.render(f, html_params).strip()
