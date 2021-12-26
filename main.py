from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
path = '/Users/libo/PycharmProjects/Finals/chromedriver'
driver = webdriver.Chrome(path)
name = input('請輸入書名')

#台北市立圖書館
driver.get('https://book.tpml.edu.tw/webpac/webpacIndex.jsp')
keyword = driver.find_element(By.CSS_SELECTOR,'#search_inputS')
keyword.send_keys(name)
keyword.submit()
iframe = driver.find_elements(By.TAG_NAME,"iframe")[0]
driver.switch_to.frame(iframe)

#book1
try:
    print('---BOOK 1---')
    a = driver.find_element(By.XPATH,'/html/body/div[2]/div[4]/table/tbody/tr[1]/td[2]/div/div[1]/a')
    a.click()
    search= driver.current_url
    url_list = search.split('=')
    key = url_list[1]
    id = key[:-6]
    book_name = driver.find_element(By.XPATH,'/html/body/div[1]/table/tbody/tr/td[1]/div/div/table/tbody/tr/td[2]/h3')
    print(book_name.text)
    url = f'https://book.tpml.edu.tw/webpac/maintain/bookDetailAssdataAjax.do?id={id}'
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    key = soup.findAll('table')
    for i in key:
        td = i.findAll('td')
        print(td[0].string, td[1].string)
    print('---館藏資訊---')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    div = soup.find('div',{'id':'integratehold'})
    head = div.findAll('th')
    tr = div.findAll('tr')
    for i in tr[1:]:
        for j in range(0,len(head)):
            body = i.findAll('td')
            print(head[j].string,':',body[j].string)
        print('-----')
    driver.back()
except:
    print('Finished')
#book2
print('---BOOK 2---')
try:
    iframe = driver.find_elements(By.TAG_NAME,"iframe")[0]
    driver.switch_to.frame(iframe)
    a = driver.find_element(By.XPATH,'/html/body/div[2]/div[4]/table/tbody/tr[3]/td[2]/div/div[1]/a')
    a.click()
    search= driver.current_url
    url_list = search.split('=')
    key = url_list[1]
    id = key[:-6]
    book_name = driver.find_element(By.XPATH,'/html/body/div[1]/table/tbody/tr/td[1]/div/div/table/tbody/tr/td[2]/h3')
    print(book_name.text)
    url = f'https://book.tpml.edu.tw/webpac/maintain/bookDetailAssdataAjax.do?id={id}'
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    key = soup.findAll('table')
    for i in key:
        td = i.findAll('td')
        print(td[0].string, td[1].string)
    print('---館藏資訊---')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    div = soup.find('div',{'id':'integratehold'})
    head = div.findAll('th')
    tr = div.findAll('tr')
    for i in tr[1:]:
        for j in range(0,len(head)):
            body = i.findAll('td')
            print(head[j].string,':',body[j].string)
        print('-----')
    driver.back()
except:
    print('Finished')
#book3
print('---BOOK 3---')
try:
    iframe = driver.find_elements(By.TAG_NAME,"iframe")[0]
    driver.switch_to.frame(iframe)
    a = driver.find_element(By.XPATH,'/html/body/div[2]/div[4]/table/tbody/tr[5]/td[2]/div/div[1]/a')
    a.click()
    search= driver.current_url
    url_list = search.split('=')
    key = url_list[1]
    id = key[:-6]
    book_name = driver.find_element(By.XPATH,'/html/body/div[1]/table/tbody/tr/td[1]/div/div/table/tbody/tr/td[2]/h3')
    print(book_name.text)
    url = f'https://book.tpml.edu.tw/webpac/maintain/bookDetailAssdataAjax.do?id={id}'
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    key = soup.findAll('table')
    for i in key:
        td = i.findAll('td')
        print(td[0].string, td[1].string)
    print('---館藏資訊---')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    div = soup.find('div',{'id':'integratehold'})
    head = div.findAll('th')
    tr = div.findAll('tr')
    for i in tr[1:]:
        for j in range(0,len(head)):
            body = i.findAll('td')
            print(head[j].string,':',body[j].string)
        print('-----')
except:
    print('Finished')
#新北市立圖書館
print('----新北市立圖書館----')
driver.get(f'https://webpac.tphcc.gov.tw/webpac/search.cfm?m=ss&k0={name}&t0=k&c0=and')

#book1
try:
    print('---BOOK 1---')
    a = driver.find_element(By.XPATH,'//*[@id="wrap"]/div[3]/div/div[2]/div[3]/div[2]/div[2]/a[2]')
    a.click()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    name = soup.find('div',{'class':'right'})
    #書名
    print('書名:',name.h2.string)
    information = soup.find('div',{'class':'detail simple'})
    key = information.findAll('p')
    for i in key:
        try:
            lista = i.string.split()
            print(lista[0],lista[1],lista[2])
        except:
            continue
    print('-----館藏地點------')
    cur_url = driver.current_url
    url_list = cur_url.split('=')
    key = url_list[1]
    id = key[:-2]
    url = f'https://webpac.tphcc.gov.tw/webpac/ajax_page/get_content_area.cfm?mid={id}&i_is=&i_lc=&i_list_number=10&i_page=1&i_vn=&i_cn=&i_ye=&i_sory_by=1'
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('thead')
    title_key = title.findAll('th')
    library = soup.find('tbody')
    library_key = library.findAll('tr')
    for i in library_key:
        key = i.findAll('td')
        j = 0
        for i in key:
            try:
                print(title_key[j].string,':',i.span.string.split()[0])
                j+=1
            except:
                continue
        print('---------------')
    driver.back()
except:
    print('Finished')
#book2
try:
    print('---BOOK 2---')
    a = driver.find_element(By.XPATH,'//*[@id="wrap"]/div[3]/div/div[2]/div[3]/div[3]/div[2]/a[2]')
    a.click()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    name = soup.find('div',{'class':'right'})
    #書名
    print('書名:',name.h2.string)
    information = soup.find('div',{'class':'detail simple'})
    key = information.findAll('p')
    for i in key:
        try:
            lista = i.string.split()
            print(lista[0],lista[1],lista[2])
        except:
            continue
    print('-----館藏地點------')
    cur_url = driver.current_url
    url_list = cur_url.split('=')
    key = url_list[1]
    id = key[:-2]
    url = f'https://webpac.tphcc.gov.tw/webpac/ajax_page/get_content_area.cfm?mid={id}&i_is=&i_lc=&i_list_number=10&i_page=1&i_vn=&i_cn=&i_ye=&i_sory_by=1'
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('thead')
    title_key = title.findAll('th')
    library = soup.find('tbody')
    library_key = library.findAll('tr')
    for i in library_key:
        key = i.findAll('td')
        j = 0
        for i in key:
            try:
                print(title_key[j].string, ':', i.span.string.split()[0])
                j += 1
            except:
                continue
        print('---------------')
    driver.back()
except:
    print('Finished')
#book3
try:
    print('---BOOK 3---')
    a = driver.find_element(By.XPATH,'//*[@id="wrap"]/div[3]/div/div[2]/div[3]/div[4]/div[2]/a[2]')
    a.click()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    name = soup.find('div',{'class':'right'})
    #書名
    print('書名:',name.h2.string)
    information = soup.find('div',{'class':'detail simple'})
    key = information.findAll('p')
    for i in key:
        try:
            lista = i.string.split()
            print(lista[0],lista[1],lista[2])
        except:
            continue
    print('-----館藏地點------')
    cur_url = driver.current_url
    url_list = cur_url.split('=')
    key = url_list[1]
    id = key[:-2]
    url = f'https://webpac.tphcc.gov.tw/webpac/ajax_page/get_content_area.cfm?mid={id}&i_is=&i_lc=&i_list_number=10&i_page=1&i_vn=&i_cn=&i_ye=&i_sory_by=1'
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('thead')
    title_key = title.findAll('th')
    library = soup.find('tbody')
    library_key = library.findAll('tr')
    for i in library_key:
        key = i.findAll('td')
        j = 0
        for i in key:
            try:
                print(title_key[j].string, ':', i.span.string.split()[0])
                j += 1
            except:
                continue
        print('---------------')
except:
    print('Finished')