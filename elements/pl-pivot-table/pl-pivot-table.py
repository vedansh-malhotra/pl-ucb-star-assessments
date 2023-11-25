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
    num_index = int(soup.find('pl-pivot-table')['index'])
    data['params']['num_index'] = num_index
    

    is_ellipsis = soup.find('pl-pivot-table')['ellipsis'] == 'true'
    is_multicol = soup.find('pl-pivot-table')['multi-col'] == 'true'
    data['params']['multi_cols'] = is_multicol
    
    col_width = {6:'2',5:'2',4:'3',3:'3',2:'3'}
    
    uuid = pl.get_uuid()
    if(is_multicol):
        answer_dic = {
            'uuid':uuid,
            'column1':list(),
            'column2':list(),
            'row':list()
        }
    else:
        answer_dic = {
            'uuid':uuid,
            'column':list(),
            'row':list()
        }

    if num_index == 1:
        answer_dic['index'] = list()
    elif num_index == 2:
        answer_dic['index1'] = list()
        answer_dic['index2'] = list()
    
    html_cols = soup.find('pl-column').find_all('pl-choice')
    lst_colset = list()

    if(is_multicol):
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
                if not 'place' in choice.attrs:
                    print("Place of column answer isn't specified")

                if choice['place'] == "1":
                    answer_dic['column1'].append(count)
                elif choice['place'] == "2":
                    answer_dic['column2'].append(count)
                
            lst_colset.append(dic_cols)
    else:
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

    if num_index == 1:

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

    elif num_index == 2:

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
                if not 'place' in choice.attrs:
                    print("Place of index answer isn't specified")

                if choice['place'] == "1":
                    answer_dic['index1'].append(count)
                elif choice['place'] == "2":
                    answer_dic['index2'].append(count)
            
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
            answer_dic['row'].append(place)
        else:
            answer_dic['row'].append(None)
        
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
            answer_row = list(map(lambda x: x-1, answer_row)) #Subtract each element by one => the attribute input starting from one: place="[1,2,3]"
            if dropzone_spot in answer_row:
                correct_count += 1
        else:
            if answer_row == None:
                continue
            answer_row -= 1
            if dropzone_spot == answer_row:
                correct_count += 1


    if correct_count == num_row_dropzone:
        final_score += 0.4

    
    data['partial_scores'][uuid] = {'score':final_score}
