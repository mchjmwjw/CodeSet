from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com/pages/page3.html')
basObj = BeautifulSoup(html, 'html.parser')

# for child in basObj.find('table', {'id': 'giftList'}).tr.next_siblings:
#     print(child)

print(basObj.table.tr)