import requests
import threading
import time
import json
import re
#from spacy.lang.en import English
from itertools import islice
import queue as Queue
import sys
def get_process(threadName, delay, output):
    url = delay.get(timeout=2)
    #nlp = English() #just the language with no model
    #entencizer = nlp.create_pipe("sentencizer")
    #nlp.add_pipe(sentencizer)
    try:
        r = requests.get(url, timeout=20)
        print(delay.qsize(), threadName, r.status_code, url)
        if(r.status_code == 200):
            text = r.text
            json_str = json.loads(text)
            response_str = json_str['full-text-retrieval-response']
            coredata_str = response_str['coredata']
            abstract_str = coredata_str['dc:description']
            openaccess_str = coredata_str['openaccess']
            #abstract_str = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','',abstract_str)
            if (openaccess_str=='1'):
                orginalText_str = response_str['originalText']
                orginalText_str = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','',orginalText_str)
                orginalText_str = re.sub('\n','',orginalText_str)
                #abstract_doc = nlp(abstract_str)
                #for sent in abstract_doc.sents:
                 #   output.write(sent.text)
                abstract_str = re.sub('\n','',abstract_str)
                output.write(abstract_str)
                output.write("\n")
                #orginalText_doc = nlp(orginalText_str)
                #for sent in orginalText_doc.sents:
                output.write(orginalText_str)
                output.write("\n")
                output.write("\n")
                #output.close()
            elif (openaccess_str=='0'):
                #abstract_doc = nlp(abstract_str)
                #for sent in abstract_doc.sents:
                abstract_str = re.sub('\n','',abstract_str)
                output.write(abstract_str)
                output.write("\n")
                output.write("\n")
            #output.close()
        print(delay.qsize(), threadName)
    except Exception as e:
        print(delay.qsize(), threadName, url, 'Error:', e)
class myThread(threading.Thread):
    def __init__(self, name, delay, output):
        threading.Thread.__init__(self)
        self.name = name
        self.delay = delay
        self.output = output
    def run(self):
        print("Starting " + self.name)
        while True:
            try:
                get_process(self.name, self.delay, self.output)
            except:
                break
        print("Exitting "+self.name)
def main( ):
    f = open(sys.argv[1], "r")
    #number_str = 10
    link_list = []
    for line in islice(f, int(sys.argv[3]), int(sys.argv[4])):
        line = line.strip()
        link_list.append(line)
    f.close()
    start = time.time()
    output = open(sys.argv[2],'w', encoding='utf-8')
    threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5","Thread-6","Thread-7","Thread-8","Thread-9","Thread-10"]
    workQueue = Queue.Queue(int(sys.argv[4])-int(sys.argv[3])+1)
    threads = []
    #创建新线程
    for tName in threadList:
        thread = myThread(tName, workQueue, output)
        thread.start()
        threads.append(thread)
    #填充队列
    for url in link_list:
        workQueue.put("https://api.elsevier.com/content/article/doi/"+url+"?apiKey="+sys.argv[5]+"&httpAccept=application%2Fjson")
    #等待所有线程完成
    for t in threads:
        t.join()
    output.close()
    end = time.time()
    print("Queue多线程爬虫的总时间为：", end-start)
if __name__ == "__main__":
    main()
"""response_str=data['full-text-retrieval-response']
orginalText_str=response_str['originalText']
coredata_str = response_str['coredata']
abstract_str = coredata_str['dc:description']
openaccess_str = coredata_str['openaccess']
print(abstract_str)
print('*************************')
print(openaccess_str)
print('########################')
print(orginalText_str)"""