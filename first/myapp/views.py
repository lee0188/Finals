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


import requests, random, time,sys, ast, traceback
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
            time.sleep(2)
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
    print(f'{value} 博客來搜尋結束')
    
    #台北市立圖書館
    driver.get('https://book.tpml.edu.tw/webpac/webpacIndex.jsp')
    keyword = driver.find_element(By.CSS_SELECTOR,'#search_inputS')
    keyword.send_keys(value)
    keyword.submit()
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    dVC = soup.find_all('div',id='detailViewDetailContent')
    len_detail = len(dVC)
    if len_detail != 0:
        print(f'{value} 北市圖只有一本館藏')
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#detailViewDetailContent > table:nth-child(1)')))
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#integratehold > table > tbody')))
        soup = BeautifulSoup(driver.page_source,'html.parser')
        TC_BookName = soup.find('h3').text
        key = dVC[0].findAll('table')
        marc = []
        for i in key:
            td_name = i.findAll('td')[0].text
            td_content = i.findAll('td')[1].text
            marc.append((td_name, td_content))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        div = soup.find('div',{'id':'integratehold'})
        head = div.findAll('th')
        tr = div.findAll('tr')
        positAll = []
        for i in tr[1:]:
            posit = []
            for j in range(0,len(head)):
                body = i.findAll('td')
                table_body = body[j].text            
                posit.append((table_body))
            positAll.append(posit)
    else:
        iframe = driver.find_elements(By.TAG_NAME,"iframe")[0]
        driver.switch_to.frame(iframe)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        totalnum = int(soup.find('em',id='totalpage').text)
        if totalnum > 0:
            if totalnum > 3:
                totalnum = 3
            html_num = [fm + 1 for fm in range(totalnum)]
            print(f'{value} 北市圖有{totalnum}本館藏')
            hrefs = ['https://book.tpml.edu.tw/webpac/' + i.a['href'] for i in soup.find_all('h4')]
            last = []
            for fm in range(totalnum):
                addup = []
                try:
                    driver.get(hrefs[fm])
                    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#detailViewDetailContent > table:nth-child(1)')))
                    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#integratehold > table > tbody')))
                    
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    TC_BookName = soup.find('h3').text
                    addup.append(TC_BookName)

                    dVC = soup.find('div',id='detailViewDetailContent')
                    key = dVC.findAll('table')
                    marc = []
                    for i in key:
                        td_name = i.findAll('td')[0].text
                        td_content = i.findAll('td')[1].text
                        marc.append((td_name, td_content))
                    addup.append(marc)

                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    div = soup.find('div',{'id':'integratehold'})
                    head = div.findAll('th')
                    tr = div.findAll('tr')
                    positAll = []
                    for i in tr[1:]:
                        posit = []
                        for j in range(0,len(head)):
                            body = i.findAll('td')
                            table_body = body[j].text            
                            posit.append((table_body))
                        positAll.append(posit)
                    addup.append(positAll)
                except:
                    print(hrefs[fm], fm)
                    print(traceback.format_exc())
                else:
                    last.append(addup)
        elif totalnum == 0:
            msg2 = f'北市圖沒有 {value} 的資料'


    #新北市立圖書館
    driver.get(f'https://webpac.tphcc.gov.tw/webpac/search.cfm?m=ss&k0={value}&t0=k&c0=and')
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    no_data_len = len(soup.find_all('p',string='無符合館藏資料'))
    if no_data_len == 0:
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="wrap"]/div[3]/div/div[2]/div[2]/div[1]/div[2]/span'))) # wait totalnum
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        page_display = soup.find('div',class_='page-display').text
        p_f = page_display.find('共') + 1
        page_display = page_display[p_f:]
        p_l = page_display.find('筆')
        page_display = int(page_display[:p_l])
        if page_display > 3:
            page_display = 3
        NT_last = []
        print(f'{value} 在新北圖有{page_display}本')
        
        hrefs = ['https://webpac.tphcc.gov.tw/webpac/' + h3.parent['href'] for h3 in soup.find_all('h3')]
        for display in range(page_display):
            try:
                addup = []
                driver.get(hrefs[display])
                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="wrap"]/div[3]/div/div[2]/div[3]/div[2]/div[2]'))) # wait detail
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                name = soup.find('div',{'class':'right'})
                NT_BookName = name.h2.text.strip(space) #書名
                addup.append(NT_BookName)
                information = soup.find('div',{'class':'detail simple'})
                allP = information.findAll('p')
                paragraphs = []
                for p in allP:
                    p_list=[i.strip(space) for i in p.text.split(chr(32)+chr(65306)+chr(32))]
                    paragraphs.append(tuple(p_list))
                addup.append(paragraphs)


                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="wrap"]/div[3]/div/div[2]/div[5]/div/table/tbody'))) #wait 館藏地點
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                title = soup.find('thead')
                title_key = title.findAll('th')
                library_key = soup.find('tbody').findAll('tr')
                NT_positAll = []
                for key in library_key:
                    tds = key.find_all('td')
                    td_list =[td.text.strip(space) for td in tds]
                    NT_positAll.append(td_list)
                addup.append(NT_positAll)
            except:
                print(hrefs[display],display)
                print(traceback.format_exc())
            else:
                NT_last.append(addup)
    elif no_data_len > 0:
        msg3 = f'新北圖沒有 {value} 的資料'
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
    exist_records = collection_table.objects.filter(uName=request.user)
    for i in exist_records:
        print(i)
        print(i.book_Name)
    print(type(exist_records))
    return render(request, 'collection.html', locals())

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





