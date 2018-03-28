# coding=utf-8
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = {'/wiki/Main_Page'}
count = all = 50
def getLinks(pageUrl):
    global pages, count, all
    if count < 1:
        return
    html = urlopen('http://en.wikipedia.org' + pageUrl)
    bsObj = BeautifulSoup(html, 'html.parser')
    try:
        print(str(bsObj.h1).encode('GBK', 'ignore'))  # .encode('GBK', 'ignore')
        print(
            str(bsObj.find(id='mw-content-text').find_all('p')[0])
            .encode('GBK', 'ignore')
        )
        print(
            str(
                bsObj.find(id='ca-edit').find('span').find('a').attrs['href']).encode('GBK', 'ignore')
        )
    except AttributeError as e:
        e = e
        # print('页面缺少属性!')

    for link in bsObj.find_all('a', href=re.compile('^(/wiki/)((?!:).)*$')):
        if count < 1:
            return
        if'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                count -= 1
                print('---------------------\n' + str(all - count) + '. ' + newPage + '\n')
                pages.add(newPage)
                getLinks(newPage)


def saveToFile(content):
    data = [line + '\n' for line in content]
    # 判断文件是否存在
    if os.access(fileDir, os.F_OK):
        f = open(fileDir, 'a')
        f.write('\n\n\n')
    else:
        f = open(fileDir, 'w')
    f.writelines(data)
    f.close()


getLinks('/wiki/Main_Page')
saveToFile(pages)