from typing import cast
import chevron
import lxml.html
import json
import pandas as pd
import numpy as np
import prairielearn as pl
import random
from bs4 import BeautifulSoup
from itertools import permutations 


def prepare(element_html, data):
    soup = BeautifulSoup(element_html)
    
    
    max_row = int(soup.find('pl-pivot-table-random')['max-row'])
    if max_row < 1 or max_row > 6:
        print("Invalid max row")
    data['params']['max_row'] = max_row

    args = soup.find('pl-pivot-table-random').text
    
    exec_variable = {'x':dict()}
    exec("x = " + args.strip(),None,exec_variable)
    args = exec_variable['x']

    num_possible_col = 0
    for key in args:
        if type(args[key]) == list:
            num_possible_col += len(args[key])
        else:
            num_possible_col += 1

    if num_possible_col > 6:
        print("Sorry the number of possible columns from operation exceeds the number this element supports. Max is 6")

    origin_df = data["params"]["orginal"]
    origin_df = pl.from_json(origin_df)
    origin_df = cast(pd.DataFrame, origin_df)

    val = args['values']
    val_random = random.sample(val, len(val))

    index = args['index']
    index_random = random.sample(index, len(index))

    dic = args['aggfunc']
    dic_random = random.sample(sorted(dic), len(dic))
    dic_random = {dic_random[count]:value for count, value in enumerate(dic.values())}


    answer_df = pd.pivot_table(origin_df, values=val_random, index=index_random,
        aggfunc=dic_random)
    
    col_answer = sorted(answer_df.columns)
    num_col = len(col_answer)
    if type(col_answer[0]) == tuple:
        is_multicol = True
    else:
        is_multicol = False
        num_col += 1


    indexname_answer = answer_df.index.names
    index_answer = sorted(answer_df.index)
    num_index = len(indexname_answer)

    row_answer = answer_df.values
    num_row = min(len(row_answer), max_row)

    is_ellipsis = soup.find('pl-pivot-table-random')['ellipsis'] == 'true'
    col_width = {6:'2',5:'2',4:'3',3:'3',2:'3'}
    
    uuid = pl.get_uuid()
    if(is_multicol): #when columns are multi-columns, num_col will be equal to num of dropzone
        answer_dic = {
            'uuid':uuid,
            'column1':list(),
            'column2':list(),
            'row':[list() for i in range(0,num_col)]
        }
    else:
        answer_dic = {
            'uuid':uuid,
            'column':list(),
            'row':[list() for i in range(0,num_col-1)]
        }

    if num_index == 1:
        answer_dic['index'] = list()
    elif num_index == 2:
        answer_dic['index1'] = list()
        answer_dic['index2'] = list()
    
    

    if(is_multicol):
        for col1, col2 in col_answer:
            answer_dic['column1'].append(col1)
            answer_dic['column2'].append(col2)
    else:
        answer_df['column'].append(answer_df.columns.name)
        for column_cell in col_answer:
            answer_dic['column'].append(column_cell)
            
    
    

    if num_index == 1:
        answer_dic['index'].append(indexname_answer)
        for index_cell in index_answer:
            answer_dic['index'].append(index_cell)

    elif num_index == 2:
        answer_dic['index1'].append(indexname_answer[0])
        answer_dic['index2'].append(indexname_answer[1])
        for index_cell in index_answer:
            answer_dic['index1'].append(index_cell[0])
            answer_dic['index2'].append(index_cell[1])


    for row in range(0,num_row):
        if is_multicol:
            for i in range(0,num_col):
                answer_dic['row'][i].append(row_answer[:,i])
        else:
            for i in range(0,num_col-1):
                answer_dic['row'][i].append(row_answer[:,i])


    lst_colset = list()
    if(is_multicol):
        answer_col_order1 = random.randint(0, 2)
        answer_col_order2 = random.randint(0, 2)
        perms1 = list(permutations(answer_dic['column1']))[1:]
        perms2 = list(permutations(answer_dic['column2']))[1:]

        for i ,perm in enumerate(random.sample(perms1,3)):
            dic_cols = dict()
            
            if i == answer_col_order1:
                dic_cols['column'] = [{'inner_html':ele} for ele in answer_dic['column1']]
                dic_cols['order_col'] = i
                
            else:
                dic_cols['column'] = [{'inner_html':ele} for ele in perm]
                dic_cols['order_col'] = i
            
            if is_ellipsis:
                dic_cols['is_ellipsis'] = {'width':col_width[num_col]}
            else:
                dic_cols['is_ellipsis'] = False

                
            lst_colset.append(dic_cols)
        answer_dic['column1'] = answer_col_order1

        for i ,perm in enumerate(random.sample(perms2,3)):
            dic_cols = dict()
            
            if i == answer_col_order2:
                dic_cols['column'] = [{'inner_html':ele} for ele in answer_dic['column2']]
                dic_cols['order_col'] = i
                
            else:
                dic_cols['column'] = [{'inner_html':ele} for ele in perm]
                dic_cols['order_col'] = i
            
            if is_ellipsis:
                dic_cols['is_ellipsis'] = {'width':col_width[num_col]}
            else:
                dic_cols['is_ellipsis'] = False

                
            lst_colset.append(dic_cols)
        answer_dic['column2'] = answer_col_order2
        
    else:
        answer_col_order = random.randint(0, 3)
        perms1 = list(permutations(answer_dic['column']))[1:]

        for i ,perm in enumerate(random.sample(perms1,4)):
            dic_cols = dict()
            
            if i == answer_col_order:
                dic_cols['column'] = [{'inner_html':ele} for ele in answer_dic['column']]
                dic_cols['order_col'] = i
                
            else:
                dic_cols['column'] = [{'inner_html':ele} for ele in perm]
                dic_cols['order_col'] = i
            
            if is_ellipsis:
                dic_cols['is_ellipsis'] = {'width':col_width[num_col]}
            else:
                dic_cols['is_ellipsis'] = False

                
            lst_colset.append(dic_cols)
        answer_dic['column'] = answer_col_order
    
        
    lst_indice_set = list()
    if num_index == 1:
        answer_index_order = random.randint(0, 3)
        perms1 = list(permutations(answer_dic['index']))[1:]

        for i ,perm in enumerate(random.sample(perms1,4)):
            dic_indice = dict()
            
            if i == answer_index_order:
                dic_indice['index'] = [{'inner_html':ele} for ele in answer_dic['index']]
                dic_indice['order_index'] = i
                dic_indice['is_ellipsis'] = is_ellipsis
                
            else:
                dic_indice['index'] = [{'inner_html':ele} for ele in perm]
                dic_indice['order_index'] = i
                dic_indice['is_ellipsis'] = is_ellipsis
            
            if is_ellipsis:
                dic_cols['is_ellipsis'] = {'width':col_width[num_col]}
            else:
                dic_cols['is_ellipsis'] = False

                
            lst_colset.append(dic_cols)
        answer_dic['index'] = answer_index_order

    elif num_index == 2:
        answer_index_order1 = random.randint(0, 3)
        answer_index_order2 = random.randint(0, 3)
        perms1 = list(permutations(answer_dic['index1']))[1:]
        perms2 = list(permutations(answer_dic['index2']))[1:]

        for i ,perm in enumerate(random.sample(perms1,4)):
            dic_indice = dict()
            
            if i == answer_index_order:
                dic_indice['index'] = [{'inner_html':ele} for ele in answer_dic['index1']]
                dic_indice['order_index'] = i
                dic_indice['is_ellipsis'] = is_ellipsis
                
            else:
                dic_indice['index'] = [{'inner_html':ele} for ele in perm]
                dic_indice['order_index'] = i
                dic_indice['is_ellipsis'] = is_ellipsis
            
            if is_ellipsis:
                dic_cols['is_ellipsis'] = {'width':col_width[num_col]}
            else:
                dic_cols['is_ellipsis'] = False

                
            lst_colset.append(dic_cols)
        answer_dic['index1'] = answer_index_order1

        for i ,perm in enumerate(random.sample(perms1,4)):
            dic_indice = dict()
            
            if i == answer_index_order:
                dic_indice['index'] = [{'inner_html':ele} for ele in answer_dic['index2']]
                dic_indice['order_index'] = i
                dic_indice['is_ellipsis'] = is_ellipsis
                
            else:
                dic_indice['index'] = [{'inner_html':ele} for ele in perm]
                dic_indice['order_index'] = i
                dic_indice['is_ellipsis'] = is_ellipsis
            
            if is_ellipsis:
                dic_cols['is_ellipsis'] = {'width':col_width[num_col]}
            else:
                dic_cols['is_ellipsis'] = False

                
            lst_colset.append(dic_cols)
        answer_dic['index2'] = answer_index_order2

        
    lst_rows = list()
    num_dropzone = len(answer_dic['row'])
    html_row_order = random.sample(range(0,num_dropzone),num_dropzone)
    for order in html_row_order:
        dic_rows = dict()
        
        dic_rows['row'] = [{'inner_html':ele} for ele in answer_dic['row'][order]]
        dic_rows['order_row'] = order
        dic_rows['is_ellipsis'] = is_ellipsis
        
        
        lst_rows.append(dic_rows)

    print(lst_colset)
    print(lst_rows)
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
    width = data['params']['df_set']['width']

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
            'width':width,
            'num_col':num_col,
            'num_row':num_row,
            'num_row_dropzone':num_raw_dropzone,
            'num_row_dropzone_val':len(num_raw_dropzone)
        }

        with open('pl-pivot-table-single.mustache', 'r') as f:
            return chevron.render(f, html_params).strip()
            
    elif num_index == 2:
        
        if int(width) >= 3:
            return_text = ' style="width: 12.499999995%; flex: 0 0 12.499%; max-width: 12.499%;"'
            #return_dic = {'calibration': return_text}
            #num_row = list(map(lambda x: return_dic,num_row))
        else:
            return_text = ' style="font-size: 10px;"'
            #return_dic = {'calibration': return_text}
            #num_row = list(map(lambda x: return_dic,num_row))

    
        html_params = {
            'question':True,
            'column_set':data['params']['df_set']['column_set'],
            'indice_set':data['params']['df_set']['indice_set'],
            'is_multicol':data['params']['multi_cols'],
            'row_set':data['params']['df_set']['row_set'],
            'uuid':data['params']['df_set']['question_uuid'],
            'width':width,
            'num_col':num_col,
            'num_row':num_row,
            'calibration':return_text,
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
            'width':width,
            'num_col':num_col,
            'num_row':num_row,
            'num_row_dropzone':num_raw_dropzone,
            'num_row_dropzone_val':len(num_raw_dropzone)
        }

        with open('pl-pivot-table-triple.mustache', 'r') as f:
            return chevron.render(f, html_params).strip()
        
        

def parse(element_html, data):
    is_multicol =  data['params']['multi_cols']
    
    if(is_multicol):
        uuid = data['params']['df_set']['question_uuid']
        default_return = '{"column1":null,"column2":null,"index":null,"row":null}'
        student_answer = data['raw_submitted_answers'].get(uuid+'-input',default_return)
        student_answer = json.loads(student_answer)
    
    else:
        uuid = data['params']['df_set']['question_uuid']
        default_return = '{"column":null,"index":null,"row":null}'
        student_answer = data['raw_submitted_answers'].get(uuid+'-input',default_return)
        student_answer = json.loads(student_answer)
    
    data['submitted_answers'] = student_answer

def grade(element_html, data):
    uuid = data['params']['df_set']['question_uuid']
    answer_dic = data['correct_answers'][uuid]
    num_row_dropzone = int(data['params']['num_col']) - 1
    is_multicol = data['params']['multi_cols']
    num_index = data['params']['num_index']
    final_score = 0
    
    if num_index == 1:
        index_submitted = data['submitted_answers']['index']
        index_submitted = int(index_submitted) if type(index_submitted) == str else None
        if index_submitted in answer_dic['index']:
            final_score += 0.3

    elif num_index == 2:
        index_submitted1 = data['submitted_answers']['index1']
        index_submitted2 = data['submitted_answers']['index2']

        index_submitted1 = int(index_submitted1) if type(index_submitted1) == str else None
        index_submitted2 = int(index_submitted2) if type(index_submitted2) == str else None

        if index_submitted1 in answer_dic['index1']:
            final_score += 0.15

        if index_submitted2 in answer_dic['index2']:
            final_score += 0.15
    
    if(is_multicol):
        col_submitted1 = data['submitted_answers']['column1']
        col_submitted2 = data['submitted_answers']['column2']

        col_submitted1 = int(col_submitted1) if type(col_submitted1) == str else None
        col_submitted2 = int(col_submitted2) if type(col_submitted2) == str else None


        if col_submitted1 in answer_dic['column1']:
            final_score += 0.15
        if col_submitted2 in answer_dic['column2']:
            final_score += 0.15
    else:
        col_submitted = data['submitted_answers']['column']
        col_submitted = int(col_submitted) if type(col_submitted) == str else None
        if col_submitted in answer_dic['column']:
            final_score += 0.3
    
    row_submitted = data['submitted_answers']['rows']
    row_submitted = list(map(lambda x: int(x) if type(x) == str else None ,row_submitted))


    correct_count = 0 #This will be counted upto the number of row dropzone(Are all row choices in dropzone correct?)
    for dropzone_spot, row_choice in enumerate(row_submitted):
        if row_choice == None or correct_count == num_row_dropzone:
            break
        
        
        answer_row = answer_dic['row'][row_choice] #List or place of valid answer spots where row_choice should be

        if type(answer_row) == list:
            answer_row = list(map(lambda x: x-1, answer_row))
            if dropzone_spot in answer_row:
                correct_count += 1
        else:
            answer_row -= 1
            if dropzone_spot == answer_row:
                correct_count += 1


    if correct_count == num_row_dropzone:
        final_score += 0.4

    
    data['partial_scores'][uuid] = {'score':final_score}
