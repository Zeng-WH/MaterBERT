import requests
import threading
import time
import json
import re
import math
from itertools import islice
import queue as Queue
import sys
def get_process(threadName, delay, output):
    url = delay.get(timeout=2)
    try:
        r = requests.get(url, timeout=20)
        print(delay.qsize(), threadName, r.status_code, url)
        if(r.status_code == 200):
            text = r.text
            json_str = json.loads(text)
            records = json_str['records']
            if(len(records)>0):
                abstract_str = None
                for i in range(len(records)):
                    abstract_str = records[i]['abstract']
                    abstract_str = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','',abstract_str)
                    abstract_str = re.sub('\n','',abstract_str)
                    output.write(abstract_str)
                    output.write("\n")
                    output.write("\n")
            else:
                print("Maybe we have some problem")

        print(delay.qsize(), threadName)

                
    except Exception as e:
        print(delay.qsize(), threadName, url, 'Error:', e)
#print(abstract)
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
        print("Exiting "+ self.name)
def main( ):
    start = time.time()
    output = open(sys.argv[1], 'w', encoding='utf-8')
    threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5","Thread-6","Thread-7","Thread-8","Thread-9","Thread-10"]
    workQueue = Queue.Queue(int(sys.argv[3])-int(sys.argv[2])+1)
    threads = []
    #创建新线程
    for tName in threadList:
        thread = myThread(tName, workQueue, output)
        thread.start()
        threads.append(thread)
    #填充队列
    request_num = math.floor((int(sys.argv[3])-int(sys.argv[2]))/int(sys.argv[4]))
    for i in range(request_num):
        p = sys.argv[4]
        s = str(i*int(p)+int(sys.argv[2]))
        workQueue.put("http://api.springernature.com/metadata/json?q=subject:"+sys.argv[5]+"&api_key="+sys.argv[6]+"&p="+p+"&s="+s)
        #threads = []
        #等待所有线程完成
    for t in threads:
        t.join()
    output.close()
    end = time.time()
    print("Queue多线程爬虫的总时间为：", end-start)
if __name__== "__main__":
    main( )

