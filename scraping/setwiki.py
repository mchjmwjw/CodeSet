from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os

pages = {'/wiki/Main_Page'}
count = all = 30
fileDir = os.curdir + '/DataFile/link.txt'
def getLinks(pageUrl):
    global pages
    global count, all
    if count < 1:
        return
    html = urlopen('https://en.wikipedia.org' + pageUrl)
    bsObj = BeautifulSoup(html, 'html.parser')
    for link in bsObj.find_all('a', href=re.compile('^(/wiki/)((?!:).)*$')):
        if count < 1:
            return
        if'href' in link.attrs:
            if (link.attrs['href'] not in pages) and count>0:
                newPage = link.attrs['href']
                pages.add(newPage)
                count -= 1
                print(str(all - count) + ': ' + newPage)                
                try:
                    getLinks(newPage)
                except:
                    continue

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