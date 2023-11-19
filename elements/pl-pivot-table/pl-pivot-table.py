from typing import cast
import chevron
import lxml.html
import json
import pandas as pd
import prairielearn as pl
from bs4 import BeautifulSoup


def prepare(element_html, data):
    soup = BeautifulSoup(element_html)
    data['params']['num_col'] = soup.find('pl-pivot-table')['col']
    data['params']['num_row'] = soup.find('pl-pivot-table')['row']
    is_ellipsis = soup.find('pl-pivot-table')['ellipsis'] == 'true'
    
    uuid = pl.get_uuid()
    answer_dic = {
        'uuid':uuid,
        'column':list(),
        'index':list(),
        'row':list()
    }
    
    html_cols = soup.find('pl-column').find_all('pl-choice')
    lst_colset = list()
    for count ,choice in enumerate(html_cols):
        dic_cols = dict()
        cell_vals = choice.text.split(' ')
        cell_vals = list(map(lambda x: x.replace('\s',' '),cell_vals))
        dic_cols['column'] = [{'inner_html':cell_val} for cell_val in cell_vals]
        dic_cols['order_col'] = count
        dic_cols['is_ellipsis'] = is_ellipsis
        if choice['correct'] == 'true':
            answer_dic['column'].append(count)
            
        lst_colset.append(dic_cols)
    
    
        
    html_indice = soup.find('pl-index').find_all('pl-choice')
    lst_indice_set = list()
    for count ,choice in enumerate(html_indice):
        dic_indice = dict()
        cell_vals = choice.text.split(' ')
        cell_vals = list(map(lambda x: x.replace('\s',' '),cell_vals))
        dic_indice['index'] = [{'inner_html':cell_val} for cell_val in cell_vals]
        dic_indice['order_index'] = count
        dic_indice['is_ellipsis'] = is_ellipsis
        if choice['correct'] == 'true':
            answer_dic['index'].append(count)
        
        lst_indice_set.append(dic_indice)
        
    html_rows = soup.find('pl-row').find_all('pl-choice')
    lst_rows = list()
    for count ,choice in enumerate(html_rows):
        dic_rows = dict()
        cell_vals = choice.text.split(' ')
        cell_vals = list(map(lambda x: x.replace('\s',' '),cell_vals))
        dic_rows['row'] = [{'inner_html':cell_val} for cell_val in cell_vals]
        dic_rows['order_row'] = count
        dic_rows['is_ellipsis'] = is_ellipsis
        if choice['correct'] == 'true':
            #which row should be placed in which place
            place = json.loads(choice['place'])
            answer_pair = (count,place)
            answer_dic['row'].append(answer_pair)
        
        lst_rows.append(dic_rows)
    
    data['params']['df_set'] = dict()
    data['params']['df_set']['column_set'] = lst_colset
    data['params']['df_set']['indice_set'] = lst_indice_set
    data['params']['df_set']['row_set'] = lst_rows
    data['params']['df_set']['question_uuid'] = uuid
    data['correct_answers'][uuid] = answer_dic


def render(element_html, data):
    num_col = int(data['params']['num_col'])
    num_col = [True for i in range(0,num_col)]
    
    num_row = int(data['params']['num_row'])
    num_row = [True for i in range(0,num_row)]
    
    num_col_row = [{'num_row':num_row,'order_col':i} for i in range(0,len(num_col)-1)]

    html_params = {
        'question':True,
        'column_set':data['params']['df_set']['column_set'],
        'indice_set':data['params']['df_set']['indice_set'],
        'row_set':data['params']['df_set']['row_set'],
        'uuid':data['params']['df_set']['question_uuid'],
        'num_col':num_col,
        'num_row':num_row,
        'num_col_row':num_col_row,
        'num_row_for_val':len(num_col_row)
    }

    with open('pl-pivot-table.mustache', 'r') as f:
        return chevron.render(f, html_params).strip()

def parse(element_html, data):
    uuid = data['params']['df_set']['question_uuid']
    default_return = '{"column":null,"index":null,"row":null}'
    student_answer = data['raw_submitted_answers'].get(uuid+'-input',default_return)
    student_answer = json.loads(student_answer)
    
    data['submitted_answers'] = student_answer

def grade(element_html, data):
    uuid = data['params']['df_set']['question_uuid']
    answer_dic = data['correct_answers'][uuid]
    num_row_place = int(data['params']['num_col']) - 1
    
    final_score = 0
    index_submitted = data['submitted_answers']['index']
    index_submitted = int(index_submitted) if type(index_submitted) == str else None
    if index_submitted in answer_dic['index']:
        final_score += 0.3
        
    col_submitted = data['submitted_answers']['column']
    col_submitted = int(col_submitted) if type(col_submitted) == str else None
    if col_submitted in answer_dic['column']:
        final_score += 0.3
    
    row_submitted = data['submitted_answers']['rows']
    row_submitted = list(map(lambda x: int(x) if type(x) == str else None ,row_submitted))
    count_correct = 0
    for row_count, place in answer_dic['row']:
        if count_correct == num_row_place:
            break
        
        if type(place) == list:
            for spot in place:
                if row_submitted[spot-1] == row_count:
                        count_correct += 1
        elif row_submitted[place-1] == row_count:
            count_correct += 1
                
    if count_correct == num_row_place:
        final_score += 0.4
    
    data['partial_scores'][uuid] = {'score':final_score}
