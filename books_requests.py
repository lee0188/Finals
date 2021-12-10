import requests
from bs4 import BeautifulSoup

# testbook's_name
keyword = 'Django'
re = requests.get(f'https://search.books.com.tw/search/query/key/{keyword}/cat/all')

soup = BeautifulSoup(re.text, 'html.parser')

for table in soup.find_all('table', id="itemlist_table", class_="table-searchlist clearfix"):
    for tbody in table.find_all('tbody'):
        print('書名: ', tbody.find_all('td')[2].find('a').text)
        print('價格: ', tbody.find_all('td')[2].find('ul', class_='list-nav clearfix').find_all('strong')[-1].text)
        print('基本資訊: ', tbody.find_all('td')[2].find('ul', class_='list-date clearfix').text.replace("\n", " ")[2:-1])
        print('圖片: ', tbody.find_all('td')[1].find('img').get("data-srcset"))
        print('----' * 7)
