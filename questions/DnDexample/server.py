import io
import pandas as pd
import prairielearn as pl
from bs4 import BeautifulSoup

answer_name = 'df'
df = pd.DataFrame({"Column1": ["Row1", "Row2", "Row3", "Row4", "Row5"],
               "Column2": ["Row1", "Row2", "Row3", "Row4", "Row5"],
               "Column3": ["Row1", "Row2", "Row3", "Row4", "Row5"],
               "Column4": ["Row1", "Row2", "Row3", "Row4", "Row5"],
               "Column5": ["Row1", "Row2", "Row3", "Row4", "Row5"]})

def generate(data):
    data['params'][answer_name] = pl.to_json(df)
    #I stored df by json because PL makes error when it's saved without any modification.
    #It seems like it only takes json format as its parameter.
    
                   
def operation(df):
    cols = df.columns.to_list()
    new_cols = cols[1:] + [cols[0]]
    answer_df = df[new_cols]
    return answer_df

def grade(data):
    html_sumbitted = data['raw_submitted_answers'][answer_name+'-input']
    soup_sumbitted = BeautifulSoup(html_sumbitted)
    
    html_answer = operation(df).to_html()
    soup_answer = BeautifulSoup(html_answer)
    
    
    len_col = len(df.index)
    
    lst_sumbitted = soup_sumbitted.find('thead').find_all('th')
    lst_sumbitted = [lst_sumbitted[i].text for i in range(1,1+len_col)]
    lst_answer = soup_answer.find('thead').find_all('th')
    lst_answer = [lst_answer[i].text for i in range(1,1+len_col)]
    
    if lst_sumbitted == lst_answer:
        data['score'] = 1
    else:
        data['score'] = 0
    
    #Below is debug code. Enjoy!
    #print(lst_sumbitted == lst_answer)
    #print(lst_sumbitted)
    #print(lst_answer)
