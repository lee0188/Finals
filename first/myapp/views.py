import abc
from django.core.checks import messages
from django.shortcuts import redirect, render
# Create your views here.
from django.http import HttpResponse, response, JsonResponse
from selenium.webdriver.common import keys
from myapp.models import student, collection_table
from myapp.form import collection_tableModelForm, RegisterForm, LoginForm
from django.contrib.auth import authenticate
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.template.defaulttags import register
from django.utils.encoding import smart_str
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


import requests, random, time,sys, ast
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common import alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
# if using mac need this
from webdriver_manager.chrome import ChromeDriverManager


# Create your views here.
##ccClub
def Chrome():
    global driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # if using mac need this
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    # driver = webdriver.Chrome(options=chrome_options)

try:
    print(driver.current_url)
except:
    Chrome()

space = chr(32)+chr(10)+chr(9)+chr(13)+chr(160)+chr(5760)+chr(6158)+chr(8194)+chr(8195)+chr(8196)+chr(8197)+\
chr(8198)+chr(8199)+chr(8200)+chr(8201)+chr(8202)+chr(8203)+chr(8204)+chr(8205)+\
chr(8239)+chr(8287)+chr(8288)+chr(12288)+chr(65279)


def browser(path):
    while True:
        try:
            driver.get(path)
            break
        except Exception as e:
            driver.quit()
            Chrome()



def delete_cookie(request,key):
    print('刪除搜尋紀錄',key)
    now_cookies=ast.literal_eval(request.COOKIES['searchword']) #<class 'list'> each element is bytes.
    en_ = key.encode('utf-8')
    if en_ in now_cookies:
        response = redirect('/')
        now_cookies.remove(en_)
        response.set_cookie('searchword',str(now_cookies))
        return response
 
#搜尋結果
def Berkeley_output(request,value):

    #博客來
    count = 0
    url = f'https://search.books.com.tw/search/query/key/{value}/cat/BKA'
    while True:  #確保搜尋有效
        try:
            browser(url)
            time.sleep(3)
            soup=BeautifulSoup(driver.page_source,'html.parser')
        except:
            pass
        else:
            none_item=soup.find_all('div',class_ = 'none clearfix') #沒搜尋結果
            search_results=soup.find_all('div',class_='search_results') #有搜尋結果
            if none_item!=[] or search_results!=[]:
                if none_item != []:
                    msg = f'博客來沒有 {value} 的資料'
                break

            else:
                print(f"{value} 博客來 搜尋結果異常")
                count+=1
                if count%2==0:
                    driver.quit()
                    Chrome()
                else:
                    driver.refresh()
    berkely_bs={}
    for table in soup.find_all('table', id="itemlist_table", class_="table-searchlist clearfix"):
        for tbody in table.find_all('tbody'):
            name = tbody.find_all('td')[2].find('a').text
            price = tbody.find_all('td')[2].find('ul', class_='list-nav clearfix').find_all('strong')[-1].text
            data = tbody.find_all('td')[2].find('ul', class_='list-date clearfix').text.replace("\n", " ")[2:-1]
            img = tbody.find_all('td')[1].find('img').get("data-srcset")
            href ='https:'+tbody.find_all('td')[2].find('a')['href']
            berkely_bs[href]={
                'name':name,
                'price':price,
                'data': data,
                'img': img,
            }
    berkely_bs = dict(list(berkely_bs.items())[:6]) #選前6本書即可
    if request.user.is_authenticated:
        for href in berkely_bs:
            exist_records = collection_table.objects.filter(uName=request.user, book_url=href, book_Name=berkely_bs[href]['name'], book_Price=int(berkely_bs[href]['price']))
            if exist_records:
                berkely_bs[href]['fav'] = "取消收藏"
            else:
                berkely_bs[href]['fav'] = "加入收藏"
    else:
        for href in berkely_bs:
            berkely_bs[href]['fav'] = "加入收藏"
    
    #台北市立圖書館
    driver.get('https://book.tpml.edu.tw/webpac/webpacIndex.jsp')
    keyword = driver.find_element(By.CSS_SELECTOR,'#search_inputS')
    keyword.send_keys(value)
    keyword.submit()
    soup=BeautifulSoup(driver.page_source,'html.parser')
    dVC = soup.find('div',id='detailViewDetailContent')
    if dVC is not None:
        TC_BookName = soup.find('h3').text
        key = dVC.findAll('table')
        marc=[]
        for i in key:
            td_name = i.findAll('td')[0].text
            td_content = i.findAll('td')[1].text
            marc.append((td_name, td_content))
        print('---館藏資訊---')

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        div = soup.find('div',{'id':'integratehold'})
        head = div.findAll('th')
        tr = div.findAll('tr')
        for i in tr[1:]:
            posit = []
            for j in range(0,len(head)-1):
                body = i.findAll('td')
                table_body = body[j].text
                if j==4:
                    if table_body=='一般書庫區':
                        posit.append((table_body))
                else:
                    posit.append((table_body))
            print(posit)
            print('-----')

    else:
        print('多本')
        #book1
        print('---BOOK 1---')
        try:
            iframe = driver.find_elements(By.TAG_NAME,"iframe")[0]
            driver.switch_to.frame(iframe)
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
                print(td[0].text, td[1].text)
            print('---館藏資訊---')
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            div = soup.find('div',{'id':'integratehold'})
            head = div.findAll('th')
            tr = div.findAll('tr')
            for i in tr[1:]:
                for j in range(0,len(head)-1):
                    body = i.findAll('td')
                    if j==4:
                        if body[j].text=='一般書庫區':
                            print(head[j].text,':',body[j].text)
                    else:
                        print(head[j].text,':',body[j].text)
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
                print(td[0].text, td[1].text)
            print('---館藏資訊---')
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            div = soup.find('div',{'id':'integratehold'})
            head = div.findAll('th')
            tr = div.findAll('tr')
            for i in tr[1:]:
                for j in range(0,len(head)-1):
                    body = i.findAll('td')
                    if j==4:
                        if body[j].text=='一般書庫區':
                            print(head[j].text,':',body[j].text)
                    else:
                        print(head[j].text,':',body[j].text)
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
                print(td[0].text, td[1].text)
            print('---館藏資訊---')
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            div = soup.find('div',{'id':'integratehold'})
            head = div.findAll('th')
            tr = div.findAll('tr')
            for i in tr[1:]:
                for j in range(0,len(head)-1):
                    body = i.findAll('td')
                    if j==4:
                        if body[j].text=='一般書庫區':
                            print(head[j].text,':',body[j].text)
                    else:
                        print(head[j].text,':',body[j].text)
                print('-----')
        except:
            print('Finished')


    return render(request, "Berkeley_output.html", locals())



#搜尋介面
def Berkeley_post(request):
    if request.COOKIES != None:
        if 'searchword' in request.COOKIES:
            bytes_list = ast.literal_eval(request.COOKIES['searchword'])
            bytes_list = [byte.decode() for byte in bytes_list]

    if request.method =='POST':
        keyword = request.POST['keyword'].strip(space)
        print('關鍵字',keyword)
        if keyword != '':

            response = redirect(f'/Berkeley_output/{keyword}')

            utf8 = keyword.encode('utf-8')
            if 'searchword' in request.COOKIES:
                cookies= request.COOKIES['searchword']
                cookies = ast.literal_eval(cookies)
                if utf8 not in cookies:
                    cookies.append(utf8)

                response.set_cookie('searchword',cookies)
            else:
                response.set_cookie('searchword',[utf8])


            return response
    else:
        pass
    return render(request,'Berkeley_post.html',locals())


# 會員註冊
def sign_up(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  #重新導向到登入畫面
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


#登入
def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  #重新導向到首頁
    context = {
        'form': form
    }
    return render(request, 'login.html', context)

# 登出
def log_out(request):
    logout(request)
    return redirect('/') #重新導向到登入畫面

def collection(request):
    return render(request, 'collection.html')

def add_fav_ajax(request):
    data = {'success': False}
    if request.method=='POST':
        bookname = request.POST.get("bookname")
        bookurl = request.POST.get("bookurl")
        bookprice = request.POST.get("bookprice", 0)
        bookinfo = request.POST.get("bookinfo")
        

        if not request.user.is_authenticated:
            data['success'] = -1
            return JsonResponse(data)

        exist_records = collection_table.objects.filter(uName=request.user, book_url=bookurl, book_Name=bookname, book_Price=bookprice)
        
        if exist_records:
            exist_records.delete()
            data['success'] = -2

        else:
            datas = {'uName': request.user, 'book_url': bookurl, 
                'book_Name': bookname, 'book_Price': int(bookprice), 'book_Info': bookinfo}
            form = collection_tableModelForm(datas)
            form.uName = request.user
            form.book_url = bookurl
            form.book_Name = bookname
            form.book_Price = int(bookprice)
            form.book_Info = bookinfo
            if form.is_valid():
                form.save()
                data['success'] = True
            else:
                print(form.errors)
                print("表單錯誤")
    return JsonResponse(data)





