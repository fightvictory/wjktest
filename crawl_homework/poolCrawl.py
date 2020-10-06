import requests
from bs4 import BeautifulSoup
import multiprocessing as mp
import re
import sys, time

sys.setrecursionlimit(1000000) 
h = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}

def parse_page(url):
    content = requests.get(url, headers=h).content
    page_books = []
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
        page_books.append(book)

    return page_books

def main(pages):
    pool = mp.Pool()
    base_url = 'http://book.zongheng.com/store/c0/c0/b0/u0/p{}/v9/s9/t0/u0/i1/ALL.html'
    
    url_list = [base_url.format(i) for i in range(1, pages + 1)]
    # for i in range(pages+1):
    #     url = base_url.format(i)
    #     url_list.append(url)
    multi_res = [pool.apply_async(parse_page, (url,)) for url in url_list ]
    pageBooks = [res.get() for res in multi_res]
    # res = multi_res[0]
    # print(res.get(timeout=1))

    books = []
    for pageBook in pageBooks:
        for book in pageBook:
            books.append(book)

    print(len(books))

if __name__ == "__main__":
    pages = int(input('请输入页码：'))
    t1 = time.time()
    main(pages)
    t2 = time.time()
    print(t2-t1)