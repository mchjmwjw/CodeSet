from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re, datetime, random

pages = set()
random.seed(datetime.datetime.now)

# 获取页面内所有内链的列表
def getInternalLinks(bsObj, includeUrl):
    # scheme='http',netloc='www.cwi.nl:80', path='/%7Eguid/Python.html', params='', query='', fragment=''
    includeUrl = urlparse(includeUrl).scheme + "://" + urlparse(includeUrl).netloc
    internalLinks = []
    # 找出所有以'/'开头的链接 或包含includeUrl的链接
    for link in bsObj.find_all('a', href=re.compile('^(/|.*' + includeUrl + ')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks

# 获取页面所有外链的列表
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    # 找出所有以'http'或'www'开头且不包含当前url的链接
    for link in baObj.find_all('a', href=re.compile('^(http|www)((?!' + excludeUrl + ').)*$')):
        if link.attrs['href'] is not in externalLinks:
            externalLinks.append(link.attrs['href'])
    return externalLinks

def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html, 'html.parser')
    externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
    if len(externalLinks) == 0:
        print('该站点不存在外链')
        domain = urlparse(startingPage).scheme + '://' + urlparse(startingPage).netloc
        internalLinks = getInternalLinks(bsObj, domain)
        internalLinks = getInternalLinks(startingPage)
        return getExternalLinks(internalLinks[random.randint(0, len(internalLinks) - 1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks) - 1)]

def followExternalOnly(startingSite):
    externalLink = getExternalLinks(startingSite)
    print("Random external link is: " + externalLink)
    followExternalOnly(externalLink)

followExternalOnly('http://oreilly.com')