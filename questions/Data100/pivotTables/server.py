import pandas as pd
import prairielearn as pl

def generate(data):
    dummy_data = {
        'Category': ['A', 'A', 'B', 'B'],
        'Item': ['X', 'Y', 'X', 'Y'],
        'Value': [10, 15, 20, 25],
        'Quantity': [100, 150, 200, 250]
    }
    input_df = pd.DataFrame(dummy_data)
    pivoted_df = input_df.pivot(index='Category', columns='Item', values=['Value', 'Quantity'])

    # Create lists of column and row labels and data values
    columns = list(pivoted_df.columns)
    index = list(pivoted_df.index)
    values = pivoted_df.values.flatten().tolist()

    data["params"]["input_df"] = pl.to_json(input_df)
    data["params"]["pivoted_df"] = pl.to_json(pivoted_df)
    data["params"]["columns"] = columns
    data["params"]["index"] = index
    data["params"]["values"] = values
