from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import requests
path = '/Users/libo/PycharmProjects/Finals/chromedriver'
driver = webdriver.Chrome(path)
name = input('請輸入書名')

#台北市立圖書館
driver.get('https://book.tpml.edu.tw/webpac/webpacIndex.jsp')
keyword = driver.find_element_by_css_selector('#search_inputS')
keyword.send_keys('原子習慣')
keyword.submit()
a = driver.find_element_by_xpath('/html/body/div[2]/div[4]/table/tbody/tr[1]/td[2]/div/div[1]/a')
a.click()

# b = driver.find_elements(By.CLASS_NAME, "usebtn")
# b[0].click()
# b[1].click()



#新北市立圖書館
#
# driver.get(f'https://webpac.tphcc.gov.tw/webpac/search.cfm?m=ss&k0={name}&t0=k&c0=and')
# a = driver.find_element_by_xpath('//*[@id="wrap"]/div[3]/div/div[2]/div[3]/div[2]/div[2]/a[2]')
# a.click()
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# name = soup.find('div',{'class':'right'})
# #書名
# print('書名:',name.h2.string)
# information = soup.find('div',{'class':'detail simple'})
# key = information.findAll('p')
# for i in key:
#     try:
#         lista = i.string.split()
#         print(lista[0],lista[1],lista[2])
#     except:
#         continue
# print('-----館藏地點------')
# cur_url = driver.current_url
# url_list = cur_url.split('=')
# key = url_list[1]
# id = key[:-2]
#
# url = f'https://webpac.tphcc.gov.tw/webpac/ajax_page/get_content_area.cfm?mid={id}&i_is=&i_lc=&i_list_number=10&i_page=1&i_vn=&i_cn=&i_ye=&i_sory_by=1'
# res = requests.get(url)
# html = res.text
# soup = BeautifulSoup(html, 'html.parser')
# library = soup.find('tbody')
# library_key = library.findAll('tr')
# for i in library_key:
#     key = i.findAll('td')
#     for i in key:
#         try:
#             print(i.span.string.split()[0])
#         except:
#             continue
#     print('---------------')