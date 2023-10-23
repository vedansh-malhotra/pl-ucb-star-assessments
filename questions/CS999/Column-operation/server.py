import io
import pandas as pd
import prairielearn as pl
from bs4 import BeautifulSoup


def generate(data):

    dataframe_name = 'df-ex'
    df = pd.DataFrame({"Column1": ["Row1", "Row2", "Row3", "Row4", "Row5"],
                   "Column2": ["Row1", "Row2", "Row3", "Row4", "Row5"],
                   "Column3": ["Row1", "Row2", "Row3", "Row4", "Row5"],
                   "Column4": ["Row1", "Row2", "Row3", "Row4", "Row5"],
                   "Column5": ["Row1", "Row2", "Row3", "Row4", "Row5"]})

    cols = df.columns.to_list()
    new_cols = cols[1:] + [cols[0]]
    answer_df = df[new_cols]
        
    data['params'][dataframe_name] = pl.to_json(df)
    data['params']['correct_answers'] = pl.to_json(answer_df)
                   
