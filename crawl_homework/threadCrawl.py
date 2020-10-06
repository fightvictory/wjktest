import threading
from queue import Queue
import requests
from bs4 import BeautifulSoup
import re, sys
import time

CRAWL_EXIT = False  # 采集队列，如果为True，表示队列页码都采集完成
# 线程采集类
class ThreadCrawl(threading.Thread):
    def __init__(self, threadName, pageQueue, dataQeueu):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.pageQueue = pageQueue
        self.dataQueue = dataQeueu

        # 请求头
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

    def run(self):
        print('启动:' + self.threadName)
        while not CRAWL_EXIT:
            try:
                page = self.pageQueue.get(False)
                url = 'http://book.zongheng.com/store/c0/c0/b0/u0/p{}/v9/s9/t0/u0/i1/ALL.html'.format(page)
                content = requests.get(url, headers=self.headers).content
                self.dataQueue.put(content)
            except Exception:
                pass

        print('结束:' + self.threadName)

PARSE_EXIT = False
# 线程解析类
class ThreadParse(threading.Thread):
    def __init__(self, threadName, dataQueue, books, lock):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.dataQeueu = dataQueue
        self.books = books
        # 互斥锁
        self.lock = lock

    def run(self):
        print('启动：' + self.threadName)
        while not PARSE_EXIT:
            try:
                content = self.dataQeueu.get(False)
                self.parse(content)
            except Exception:
                pass
        print('结束:' + self.threadName)

    def parse(self, content):
        soup = BeautifulSoup(content, 'html5lib')
        store_collist = soup.find('div', class_='store_collist')

        pattern = re.compile(r'bookbox f(.)')
        book_list = store_collist.find_all('div', class_=pattern)

        for item in book_list:
            book = {}
            book['bookimg'] = item.find('div', class_='bookimg').find('img')['src']
            bookinfo = item.find('div', class_='bookinfo')
            book['bookname'] = bookinfo.find('div', class_='bookname').find('a').text
            book['bookintro'] = bookinfo.find('div', class_='bookintro')

            with self.lock:
                self.books.append(book)

def main(pages):
    

    # 页码队列
    pageQueue = Queue(pages)  # 创建page队列，队列长度为pages这么长
    for i in range(1, pages + 1):
        pageQueue.put(i)

    # 数据队列，每项的内容就是 content, 即网页的源码
    dataQueue = Queue()
    # 存放图书数据的列表
    books = []
    # 互斥锁
    lock = threading.Lock()

    # 采集线程的名字
    crawlList = ['采集1#', '采集2#', '采集3#', '采集4#']
    # 创建和启动采集线程
    threadCrawls = []
    for threadName in crawlList:
        thread = ThreadCrawl(threadName, pageQueue, dataQueue)
        thread.start()
        threadCrawls.append(thread)
    # 解析线程的名字
    parseList = ['解析1#', '解析2#', '解析3#', '解析4#']
    # 创建和启动解析线程
    threadParses = []
    for threadName in parseList:
        thread = ThreadParse(threadName, dataQueue, books, lock)
        thread.start()
        threadParses.append(thread)

    while not pageQueue.empty():
        pass

    global CRAWL_EXIT
    CRAWL_EXIT = True
    print('pageQueue为空')
    for thread in threadCrawls:
        thread.join()

    while not dataQueue.empty():
        pass

    global PARSE_EXIT
    PARSE_EXIT = True
    print('dataQueue为空')
    for thread in threadParses:
        thread.join()
    
    print(len(books))

if __name__ == "__main__":
    try:
        pages = int(input('请输入要爬到多少页：'))
    except Exception:
        print('输入的必须是大于0的整数')
        sys.exit()
    t1 = time.time()
    main(pages)
    t2 = time.time()
    print(t2-t1)