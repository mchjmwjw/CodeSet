from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen('http://en.wikipedia.org/wiki/Kevin_Bacon')
bsObj = BeautifulSoup(html, 'html.parser')
# for link in bsObj.find_all('a'):
#     if 'href' in link.attrs:
#        print(link.attrs['href'])

obj = bsObj.find('div', {'id': 'bodyContent'}).find_all(
    'a', href = re.compile('^(/wiki/)((?!:).)*$'))
for link in obj:
    if'href' in link.attrs:
        print(link.attrs['href'])