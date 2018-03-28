from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
bsObj = BeautifulSoup(html, 'html.parser')

nameList = bsObj.find_all('span', {'class': 'green'})
allText = bsObj.findAll(id='text')
# bsObj.findAll('', {'class': 'green'})
# bsObj.findAll(class_='green')
for name in nameList:
    print(name.get_text())
print(allText[0].get_text())

