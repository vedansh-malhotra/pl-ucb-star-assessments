from typing import cast
import chevron
import lxml.html
import pandas as pd
import prairielearn as pl
from bs4 import BeautifulSoup


def render(element_html: str, data: pl.QuestionData) -> str:

    element = lxml.html.fragment_fromstring(element_html)
    dataframe_name = pl.get_string_attrib(element, 'dataframe-name')
    operation = element.text_content()
    
    frame = pl.from_json(data['params'][dataframe_name])
    frame = cast(pd.DataFrame, frame)
    
    html_params = {
        'question': True,
        'dataframe_name': dataframe_name,
        'frame_html': frame.to_html(),
        'operation': operation
    }

    with open('pl-drag-drop.mustache', 'r', encoding='utf-8') as f:
        html = chevron.render(f, html_params)
    return html

def grade(element_html: str, data: pl.QuestionData):
    
    element = lxml.html.fragment_fromstring(element_html)
    dataframe_name = pl.get_string_attrib(element, 'dataframe-name')
    
    #Load submitted dataframe from parameters and parse into bs4
    html_sumbitted = data['raw_submitted_answers'][dataframe_name+'-input']
    soup_sumbitted = BeautifulSoup(html_sumbitted)
    soup_sumbitted.find('tbody').find_all('tr')

    
    #Load answer dataframe from parameters and parse into bs4
    answer_frame = pl.from_json(data['params']['correct_answers'])
    answer_frame = cast(pd.DataFrame, answer_frame)
    html_answer = answer_frame.to_html()
    soup_answer = BeautifulSoup(html_answer)
    soup_answer.find('tbody').find_all('tr')
        
    #Check whether columns are correct
    len_row = len(answer_frame.index)
    submitted = soup_sumbitted.find('tbody').find_all('tr')
    submitted = [submitted[i].find('th').text for i in range(0,len_row)]
    answer = soup_answer.find('tbody').find_all('tr')
    answer = [answer[i].find('th').text for i in range(0,len_row)]
    
    #Check whether columns are correct
    len_col = len(answer_frame.columns)
    lst_sumbitted = soup_sumbitted.find('thead').find_all('th')
    lst_sumbitted = [lst_sumbitted[i].text for i in range(1,1+len_col)]
    lst_answer = soup_answer.find('thead').find_all('th')
    lst_answer = [lst_answer[i].text for i in range(1,1+len_col)]
    
    
    if (lst_sumbitted == lst_answer) and (answer == submitted):
        score = 1
    else:
        score = 0

    
    data['partial_scores'][dataframe_name] = {
        'score': score
    }
