from typing import cast
import chevron
import lxml.html
import json
import pandas as pd
import prairielearn as pl
from bs4 import BeautifulSoup


def prepare(element_html, data):
    soup = BeautifulSoup(element_html)
    
    num_col = int(soup.find('pl-pivot-table')['col'])
    if num_col < 2:
        print("Invalid column number")
    data['params']['num_col'] = num_col
    
    num_row = int(soup.find('pl-pivot-table')['row'])
    if num_row < 1:
        print("Invalid row number")
    data['params']['num_row'] = num_row
    
    #num_index won't be refered in this function again, so there is no declaration of it
    data['params']['num_index'] = int(soup.find('pl-pivot-table')['index'])
    
    is_ellipsis = soup.find('pl-pivot-table')['ellipsis'] == 'true'
    is_multicol = soup.find('pl-pivot-table')['multi-col'] == 'true'
    data['params']['multi_cols'] = is_multicol
    
    col_width = {6:'2',5:'2',4:'3',3:'3',2:'3'}
    
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
        
        condition1 = (is_ellipsis and (len(cell_vals) == (num_col-1))) #With ellipsis, number of columns data should be num_col-1
        condition2 = ((not is_ellipsis) and (len(cell_vals) == (num_col)))#Without ellipsis, number of columns data should be num_col
        if not(condition1 or condition2):
            print("Number of columns should be equal to attribute setting")
        
        
        dic_cols['column'] = [{'inner_html':cell_val} for cell_val in cell_vals]
        dic_cols['order_col'] = count
    
        if is_ellipsis:
            dic_cols['is_ellipsis'] = {'width':col_width[num_col]}
        else:
            dic_cols['is_ellipsis'] = False
            
        if choice['correct'] == 'true':
            answer_dic['column'].append(count)
            
        lst_colset.append(dic_cols)
    
    
        
    html_indice = soup.find('pl-index').find_all('pl-choice')
    lst_indice_set = list()
    for count ,choice in enumerate(html_indice):
        dic_indice = dict()
        cell_vals = choice.text.split(' ')
        cell_vals = list(map(lambda x: x.replace('\s',' '),cell_vals))
        
        #Index needs one more text chunk than row, because it has index-label cell
        condition1 = (is_ellipsis and (len(cell_vals) == (num_row))) #With ellipsis, number of columns data should be num_col
        condition2 = ((not is_ellipsis) and (len(cell_vals) == (num_row + 1)))#Without ellipsis, number of columns data should be num_col + 1
        if not(condition1 or condition2):
            print("Number of indice should be equal to attribute setting")
        
        
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
        
        condition1 = (is_ellipsis and (len(cell_vals) == (num_row-1))) #With ellipsis, number of columns data should be num_col-1
        condition2 = ((not is_ellipsis) and (len(cell_vals) == (num_row)))#Without ellipsis, number of columns data should be num_col
        if not(condition1 or condition2):
            print("Number of rows should be equal to attribute setting")
            

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
    data['params']['df_set']['width'] = col_width[num_col]
    data['params']['df_set']['question_uuid'] = uuid
    data['correct_answers'][uuid] = answer_dic


def render(element_html, data):
    num_index = data['params']['num_index']
    num_col = data['params']['num_col']
    num_col = [True for i in range(0,num_col)]

    num_row = data['params']['num_row']
    num_row = [True for i in range(0,num_row+1)]

    num_raw_dropzone = [{'order_zone':i} for i in range(0,len(num_col)-1)]

    if num_index == 1:
    
        html_params = {
            'question':True,
            'column_set':data['params']['df_set']['column_set'],
            'indice_set':data['params']['df_set']['indice_set'],
            'is_multicol':data['params']['multi_cols'],
            'row_set':data['params']['df_set']['row_set'],
            'uuid':data['params']['df_set']['question_uuid'],
            'width':data['params']['df_set']['width'],
            'num_col':num_col,
            'num_row':num_row,
            'num_row_dropzone':num_raw_dropzone,
            'num_row_dropzone_val':len(num_raw_dropzone)
        }

        with open('pl-pivot-table-single.mustache', 'r') as f:
            return chevron.render(f, html_params).strip()
            
    elif num_index == 2:
    
        html_params = {
            'question':True,
            'column_set':data['params']['df_set']['column_set'],
            'indice_set':data['params']['df_set']['indice_set'],
            'is_multicol':data['params']['multi_cols'],
            'row_set':data['params']['df_set']['row_set'],
            'uuid':data['params']['df_set']['question_uuid'],
            'width':data['params']['df_set']['width'],
            'num_col':num_col,
            'num_row':num_row,
            'num_row_dropzone':num_raw_dropzone,
            'num_row_dropzone_val':len(num_raw_dropzone)
        }

        with open('pl-pivot-table-double.mustache', 'r') as f:
            return chevron.render(f, html_params).strip()
            
    elif num_index == 3:

        html_params = {
            'question':True,
            'column_set':data['params']['df_set']['column_set'],
            'indice_set':data['params']['df_set']['indice_set'],
            'is_multicol':data['params']['multi_cols'],
            'row_set':data['params']['df_set']['row_set'],
            'uuid':data['params']['df_set']['question_uuid'],
            'num_col':num_col,
            'num_row':num_row,
            'num_col_row':num_col_row,
            'num_row_for_val':len(num_col_row)
        }

        with open('pl-pivot-table-triple.mustache', 'r') as f:
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
