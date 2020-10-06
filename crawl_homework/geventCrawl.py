import requests
from queue import Queue
from bs4 import BeautifulSoup
import re
import gevent
import time

class Spider:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
        # 基准网扯
        self.base_url = 'http://book.zongheng.com/store/c0/c0/b0/u0/p{}/v9/s9/t0/u0/i1/ALL.html'
        # 数据队列
        self.data_queue = Queue()
        # 统计数量
        self.count = 0

        self.books = []
    
    # 发送请求的方法
    def send_request(self, url):
        # print('正在爬取：' + url)
        content = requests.get(url, headers=self.headers).content
        self.parse_page(content)

    def parse_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        store_collist = soup.find('div', class_='store_collist')

        pattern = re.compile(r'bookbox f(.)')
        book_list = store_collist.find_all('div', class_=pattern)

        for item in book_list:
            book = {}
            book['bookimg'] = item.find('div', class_='bookimg').find('img')['src']
            bookinfo = item.find('div', class_='bookinfo')
            book['bookname'] = bookinfo.find('div', class_='bookname').find('a').text
            book['bookintro'] = bookinfo.find('div', class_='bookintro')

            self.count += 1
            self.data_queue.put(book)

    def start_work(self, pageNum):
        job_list = []
        for page in range(1, pageNum + 1):
            url = self.base_url.format(page)
            # 创建协程任务
            job = gevent.spawn(self.send_request, url)
            # 把所有的协程任务加入任务列表
            job_list.append(job)
            # 等待所有的协程任务执行完毕
        gevent.joinall(job_list)

        while not self.data_queue.empty():
            book = self.data_queue.get()
            self.books.append(book)

        print(self.count)

if __name__ == "__main__":
    pages = int(input('输入页码：'))
    t1 = time.time()
    spider = Spider()
    spider.start_work(pages)
    print()
    t2 = time.time()
    print(t2-t1)
