import re
#import numpy as np
import sys
import time
import sys
from spacy.lang.en import English
import queue as Queue
from tqdm import tqdm
'''nlp = English()
sentencizer = nlp.create_pipe("sentencizer")
nlp.add_pipe(sentencizer)
output = open('output13.txt', 'w', encoding='utf-8')
with open('test.txt', 'r', encoding='utf-8') as f:
    while True:
        temp = f.readline()
        if not temp:
            break
        temp = re.sub('Fig\.\s[0-9a-zA-Z]*', 'Fig', temp) #将Fig. 全部换成Fig
        temp = re.sub('serial\sJL\s[0-9\s]*', '', temp) #去除开头的版权信息
        #ret = re.search('[a-z]', 'oewov')
        temp = re.sub('[A-Z]{10,}', '',temp) #去除大写的无意义的字符串
        #ret = re.match('\([\s\S]*\,\s[0-9]{4}\)',temp)
        #print(ret)
        temp = re.sub('[0-9]{4}-[0-9]{2}-[0-9]{2}', '', temp) #去除部分日期
        temp = re.sub('\(Table\s[0-9]*\)', '', temp) #去除table
        temp = re.sub('[\w\-\.]*(\.jpg|\.jag|\.sml|\.jpeg|\.png|\.kml)', '', temp)
        temp = re.sub('(jpg|jag|sml|jpeg|png)', '', temp)
        temp = re.sub('IMAGE\-','', temp)
        #temp = re.sub('\([\s\S]*,\s[0-9]{4}\)')
        temp = re.sub('\set\sal\.','',temp)
        temp = re.sub('gr[0-9]*', '', temp)
        temp = re.sub('[0-9]{1,}:[0-9]{1,}:[0-9]{1,}','', temp)
        temp = re.sub('[0-9]{3,}\s[0-9]{2,}\s[0-9]{2,}','' , temp)
        temp = re.sub('\([a-z0-9]*\)','', temp)
        temp = re.sub('THUMBNAIL','', temp)
        temp = re.sub('HIGH-RES', '', temp)
        temp = re.sub('^([\u4e00-\u9fa5]{2,20}|[a-zA-Z.\s]{2,20})$', '', temp)
        temp = re.sub('Abstract', '', temp)
        temp = re.sub('Fig', '', temp)
        temp = re.sub('\n','',temp)
        #temp = re.sub('\s', '', temp)
        temp = re.sub('Table\s[0-9]*\s','',temp)
        abstract_doc = nlp(temp)
        for sent in abstract_doc.sents:
            output.write(sent.text)
            output.write('\n')
        #output.write(temp)

output.close()'''
def get_process(delay, input_dir, output_dir):
    txt_str = delay.get(timeout=2)
    print("Start processing "+input_dir+txt_str+'.txt '+"now")
    nlp = English() #just the language with no model
    sentencizer = nlp.create_pipe("sentencizer")
    nlp.add_pipe(sentencizer)
    output = open(output_dir + txt_str +'pre.txt', 'w', encoding='utf-8')
    with open(input_dir + txt_str + '.txt', 'r', encoding='utf-8') as f: #打开文件
        while True:
            temp = f.readline()
            if not temp:
                break
            temp = re.sub('Fig\.\s[0-9a-zA-Z]*', 'Fig', temp)  # 将Fig. 全部换成Fig
            temp = re.sub('serial\sJL\s[0-9\s]*', '', temp)  # 去除开头的版权信息
            # ret = re.search('[a-z]', 'oewov')
            temp = re.sub('[A-Z]{10,}', '', temp)  # 去除大写的无意义的字符串
            # ret = re.match('\([\s\S]*\,\s[0-9]{4}\)',temp)
            # print(ret)
            temp = re.sub('[0-9]{4}-[0-9]{2}-[0-9]{2}', '', temp)  # 去除部分日期
            temp = re.sub('\(Table\s[0-9]*\)', '', temp)  # 去除table
            temp = re.sub('[\w\-\.]*(\.jpg|\.jag|\.sml|\.jpeg|\.png|\.kml)', '', temp)
            temp = re.sub('(jpg|jag|sml|jpeg|png)', '', temp)
            temp = re.sub('IMAGE\-', '', temp)
            # temp = re.sub('\([\s\S]*,\s[0-9]{4}\)')
            temp = re.sub('\set\sal\.', '', temp)
            temp = re.sub('gr[0-9]*', '', temp)
            temp = re.sub('[0-9]{1,}:[0-9]{1,}:[0-9]{1,}', '', temp)
            temp = re.sub('[0-9]{3,}\s[0-9]{2,}\s[0-9]{2,}', '', temp)
            temp = re.sub('\([a-z0-9]*\)', '', temp)
            temp = re.sub('THUMBNAIL', '', temp)
            temp = re.sub('HIGH-RES', '', temp)
            temp = re.sub('^([\u4e00-\u9fa5]{2,20}|[a-zA-Z.\s]{2,20})$', '', temp)
            temp = re.sub('Abstract', '', temp)
            temp = re.sub('Fig', '', temp)
            temp = re.sub('\n', '', temp)
            # temp = re.sub('\s', '', temp)
            temp = re.sub('Table\s[0-9]*\s', '', temp)
            abstract_doc = nlp(temp)
            for sent in abstract_doc.sents:
                output.write(sent.text)
                output.write('\n')
    output.close()
    print("end processing "+input_dir+txt_str+'.txt ')

def main( ):
    start = time.time()
    workQueue = Queue.Queue(int(sys.argv[2])-int(sys.argv[1])+1)
    queue_size = int(sys.argv[2]) - int(sys.argv[1]) + 1
    for i in range(queue_size):
        workQueue.put(str(int(sys.argv[1]) + i))
    for i in range(queue_size):
        get_process(workQueue, sys.argv[3], sys.argv[4])
    end = time.time()
    print("代码执行时间为：", end-start)
if __name__ == '__main__':
    main( )

#f = open('test.txt', 'r', encoding='utf-8')
#print(f.readlines())
#print('bupt')