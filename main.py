import requests
from bs4 import BeautifulSoup

#台北市立圖書館
# url = 'https://book.tpml.edu.tw/webpac/maintain/bookDetailAssdataAjax.do?id=812217'
# res = requests.get(url)
# html = res.text
# soup = BeautifulSoup(html, 'html.parser')
# key = soup.findAll('table')
# for i in key:
#     td = i.findAll('td')
#     print(td[0].string, td[1].string)

#新北市立圖書館

url = 'https://webpac.tphcc.gov.tw/webpac/content.cfm?mid=825199&m=ss&k0=%E5%8E%9F%E5%AD%90%E7%BF%92%E6%85%A3&t0=k&c0=and&list_num=10&current_page=1&mt=&at=&sj=&py=&pr=&it=&lr=&lg=&si=1&view=d'
res = requests.get(url)
html = res.text
soup = BeautifulSoup(html, 'html.parser')
name = soup.find('div',{'class':'right'})
#書名
# print(name.h2.string)
# information = soup.find('div',{'class':'detail simple'})
# key = information.findAll('p')
# for i in key:
#     print(i.string)

url = 'https://webpac.tphcc.gov.tw/webpac/ajax_page/get_content_area.cfm?mid=825199&i_is=&i_lc=&i_list_number=10&i_page=1&i_vn=&i_cn=&i_ye=&i_sory_by=1'
res = requests.get(url)
html = res.text
soup = BeautifulSoup(html, 'html.parser')
library = soup.find('tbody')
library_key = library.findAll('tr')
for i in library_key:
    key = i.findAll('td')
    for i in key:
        try:
            print(i.span.string)
        except:
            continue



