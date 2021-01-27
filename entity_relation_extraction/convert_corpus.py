import glob
import numpy as np
import json

'''将MSP的语料库转化成模型可以识别的格式'''


def find_all(sub, s):
    '''找寻字符串s中中的子字符串sub的位置'''
    index_list = []
    index = s.find(sub)
    while index != -1:
        index_list.append(index)
        index = s.find(sub, index + 1)

    if len(index_list) > 0:
        return index_list
    else:
        return -1


def convert_sentence(text):
    '''对字符文本基于'. '进行分割，并将字符的位置与词语的位置进行映射 '''
    space_all = find_all(' ', text)
    sent_all = find_all('. ', text)
    sent_all.append(10000000)
    sent_list = []
    for i in range(len(sent_all) - 1):
        temp_list = []
        temp_list.append(sent_all[i] + 1)
        for j in space_all:
            if j >= sent_all[i] and j <= sent_all[i + 1]:
                temp_list.append(j + 1)
        sent_list.append(temp_list)
    for sent_line in sent_list:
        del sent_line[0]
    return sent_list

def convert_ann2entity(ann):
    '''从ann文件中提取出实体'''
    ann_list = ann.split('\n')
    entity_list = []
    for ann_line in ann_list:
        ann_line = ann_line.split('\t')
        if len(ann_line) > 2:
            if ann_line[0][0] == 'T':
                entity_list.append(ann_line)
    return entity_list

def convert_ann2relation(ann):
    '''从ann文件中提取出实体之间的关系'''
    ann_list = ann.split('\n')
    relation_list = []
    for ann_line in ann_list:
        ann_line = ann_line.split('\t')
        if len(ann_line) > 2:
            if ann_line[0][0] == 'R':
                relation_list.append(ann_line)
    return relation_list

def convert_entity_char2vocab(text, sent_list, entity_list):
    line_split = find_all('. ', text)
    text_split = text.split('. ')
    line_split.append(10000000)
    entity_result = []
    entity_dict = {}
    for i in range(len(sent_list)):
        entity_result.append([])
    for temp_entity in entity_list:
        temp_result = {}
        dict_temp = []
        temp = (temp_entity[1]).split(' ')
        start_temp = int(temp[1])
        end_temp = int(temp[2])
        if start_temp < line_split[0]:
            continue
        temp_result['type'] = temp[0]
        for row_index, row in enumerate(line_split):
            if start_temp < row:
                break
        dict_temp.append(row_index - 1)
        for start_word, ele in enumerate(sent_list[row_index - 1]):
            if ele == start_temp:
                temp_result['start'] = start_word
        for end_word, ele in enumerate(sent_list[row_index-1]):
            if end_temp < ele:
                temp_result['end'] = end_word + 1
                if end_word==0:
                    print(end_word)
                break
        if end_temp > sent_list[row_index-1][-1]:
            temp_result['end'] = len(sent_list[row_index-1])
        entity_result[row_index-1].append(temp_result)
        dict_temp.append(len(entity_result[row_index-1])-1)
        entity_dict[temp_entity[0]] = dict_temp

    return entity_result, entity_dict

def convert_entity_with_relation(relation, sent_list, entity_dict):
    relation_result = []
    for i in range(len(sent_list)):
        relation_result.append([])
    for relation_line in relation:
        temp = (relation_line[1]).split(' ')
        if temp[1][5] == 'T' and temp[2][5] == 'T':
            arg1_temp = temp[1][5:]
            arg2_temp = temp[2][5:]
            try:
                if entity_dict[arg1_temp][0] == entity_dict[arg2_temp][0]:
                    temp_dict = {}
                    temp_dict['type'] = temp[0]
                    temp_dict['head'] = entity_dict[arg1_temp][1]
                    temp_dict['tail'] = entity_dict[arg2_temp][1]
                    relation_result[entity_dict[arg1_temp][0]].append(temp_dict)
            except KeyError:
                continue
    return relation_result

def joint_entity_relation_token(text, entity_result, relation_result, id, documents):
    text_line = text.split('. ')
    for i in range(len(entity_result)):
        id = id + 1
        document_dict = {}
        document_dict['tokens'] = (text_line[i+1]).split(' ')
        document_dict['entities'] = entity_result[i]
        document_dict['relations'] = relation_result[i]
        document_dict['orig_id'] = id
        documents.append(document_dict)
    return documents

documents =[]
textfiles = glob.glob('/home1/wlw2020/head_motion/SpERT/corpus/data/*.txt')
index = 1
for text_file in textfiles:
    temp = text_file.split('.txt')
    ann_temp = temp[0]
    ann_file = ''.join([ann_temp, '.ann'])
    with open(text_file) as f1:
        text = f1.read()
    with open(ann_file) as f2:
        ann = f2.read()
    sent_list = convert_sentence(text)
    entity_list = convert_ann2entity(ann)
    relation = convert_ann2relation(ann)
    entity_result, entity_dict = convert_entity_char2vocab(text, sent_list, entity_list)
    relation_result = convert_entity_with_relation(relation, sent_list, entity_dict)
    documents = joint_entity_relation_token(text, entity_result, relation_result, index, documents)
for document in documents:
    if len(document['tokens']) <= 2:
        documents.remove(document)
for document in documents:
    if len(document['tokens']) <= 2:
        documents.remove(document)
for i in documents:
    for j in i['entities']:
        if (len(j)) < 3:
            j['start'] = j['end'] - 1
with open('./documents_example_v3.json', 'w') as f3:
    json.dump(documents, f3)
print('iu')
