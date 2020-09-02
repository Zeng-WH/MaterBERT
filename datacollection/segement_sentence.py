import threading
import time
from spacy.lang.en import English
import sys
import queue as Queue
def get_process(threadName, delay):
    txt_str = delay.get(timeout=2)
    nlp = English() #just the language with no model
    sentencizer = nlp.create_pipe("sentencizer")
    nlp.add_pipe(sentencizer)
    output = open(txt_str+'pre.txt')
    with open(txt_str+'.txt', "r") as f: #打开文件
        data = f.read() #读取文件
        abstract_doc = nlp(data)
        for sent in abstract_doc.sents:
            output.write(sent)
    output.close()
    print(delay.qsize(), threadName)
class myThread(threading.Thread):
    def __init__(self, name, delay):
        threading.Thread.__init__(self)
        self.name=name
        self.delay=delay
    def run(self):
        print("Starting "+self.name)
        while True:
            try:
                get_process(self.name,self.delay)
            except:
                break
        print("Exiting "+self.name)
def main( ):
    start = time.time()
    threadList = ["Thread-1","Thread-2","Thread-3","Thread-4","Thread-5"]
    workQueue = Queue.Queue(int(sys.argv[2])-int(sys.argv[1])+1)
    threads = []
    #创建新线程
    for tName in threadList:
        thread = myThread(tName, workQueue)
        thread.start()
        threads.append(thread)
    # 填充队列
    queue_size = int(sys.argv[2]) - int(sys.argv[1]) + 1
    for i in range(queue_size):
        #print(str(int(sys.argv[7])+i))
        workQueue.put(str(int(sys.argv[1])+i))
    #等待所有线程完成
    for t in threads:
        t.join()
    end = time.time()
    print("代码执行时间为：", end-start)
if __name__ == '__main__':
    main( )