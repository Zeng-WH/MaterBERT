import paramiko
import threading
import time
import queue as Queue
import sys
def log_in(host, port, username, password):
    #获取Transport实例
    tran = paramiko.Transport((host, port))
    #连接SSH服务端， 使用password
    tran.connect(username= username, password=password)
    #stp = paramiko.SFTPClient.from_transport(tran)
    return tran
#设置上传的本地/远程文件路径
def sftp_download(tran, local_dir, remote_dir, localnumQueue):
    stp = paramiko.SFTPClient.from_transport(tran)
    numq = localnumQueue.get(timeout=2)
    remotepath = remote_dir + '/' + numq + '.txt'
    localpath = local_dir + '/' + numq + '.txt'
    print(remotepath)
    print(localpath)
    stp.get(remotepath, localpath)
class myThread(threading.Thread):
    def __init__(self, name, numQueue, tran, local_dir, remote_dir):
        threading.Thread.__init__(self)
        self.name = name
        self.numQueue = numQueue
        self.tran = tran
        self.local_dir = local_dir
        self.remote_dir = remote_dir
    def run(self):
        print("Starting "+ self.name)
        while True:
            try:
            #print('**********')
                sftp_download(self.tran, self.local_dir, self.remote_dir, self.numQueue)
            #print('##########')
            except:
                break
        print("Exiting "+ self.name)
def main( ):
    start = time.time()
    threadList = ["Thread-1", "Thread-2", "Thread-3","Thread-4", "Thread-5", "Thread-6", "Thread-7", "Thread-8"]
    workQueue = Queue.Queue(int(sys.argv[8])-int(sys.argv[7])+1)
    threads = []
    #创建新线程
    host = sys.argv[1]
    port = int(sys.argv[2])
    username = sys.argv[3]
    password = sys.argv[4]
    try:
        tran = log_in(host, port, username, password)
    except Exception as e:
        print("Maybe we have some problem!")
    for tName in threadList:
        thread = myThread(tName, workQueue, tran, sys.argv[5], sys.argv[6])
        thread.start()
        threads.append(thread)
    #填充队列
    queue_size = int(sys.argv[8]) - int(sys.argv[7])+1
    for i in range(queue_size):
        print(str(int(sys.argv[7])+i))
        workQueue.put("output"+str(int(sys.argv[7])+i))
    #等待所有线程完成
    for t in threads:
        t.join()
    tran.close()
    end = time.time()
    print("代码执行时间为：", end-start)
if __name__ == '__main__':
    main( )
