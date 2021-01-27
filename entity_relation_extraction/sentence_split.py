from spacy.lang.en import English
from tqdm import tqdm

def find_all(sub, s):
    index_list = []
    index = s.find(sub)
    while index != -1:
        index_list.append(index)
        index = s.find(sub, index + 1)

    if len(index_list) > 0:
        return index_list
    else:
        return -1
def process_sentence(input_dir):
    sentence_list = []
    nlp = English()
    sentencizer = nlp.create_pipe("sentencizer")
    nlp.add_pipe(sentencizer)
    with open(input_dir, 'r') as f: #打开文件
        data = f.readlines() #读取文件
        for line in tqdm(data):
            doc = nlp(line)
            for sent in doc.sents:
                sentence_list.append(sent.text)
                #print(len(sent.text))
    return sentence_list

def convert_sentence(text, sentence_list):
    sen_index = []
    for i in range(len(sentence_list)-1):
        if i == 0:
            sen_index.append(len(sentence_list[i]))
        else:
            sen_index.append(len(sentence_list[i])+sen_index[-1])

    print('tu')

def convert_sentence_new(text):
    #基于'. '来分割句子
    space_all = find_all(' ', text)
    sent_all = find_all('. ', text)
    sent_all.append(10000000)
    sent_list = []
    for i in range(len(sent_all) - 1):
        temp_list = []
        temp_list.append(sent_all[i]+1)
        for j in space_all:
            if j>= sent_all[i] and j<= sent_all[i + 1]:
                temp_list.append(j+1)
        sent_list.append(temp_list)
    return sent_list

with open('./mspcorpus/101039c7ta03087h.txt') as f1:
    text = f1.read()
test_index, test = convert_sentence_new(text)
a = text[test_index[0][0]]
b = text[test_index[0][1]]
c = text[test_index[-1][1]]
for test_index_line in test_index:
    del test_index_line[0]
a1 = text[test_index[0][0]]
b1 = text[test_index[1][0]]

print('bupt')






