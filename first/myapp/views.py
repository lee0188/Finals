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
    print('??????????????????',key)
    now_cookies=ast.literal_eval(request.COOKIES['searchword']) #<class 'list'> each element is bytes.
    en_ = key.encode('utf-8')
    if en_ in now_cookies:
        response = redirect('/')
        now_cookies.remove(en_)
        response.set_cookie('searchword',str(now_cookies))
        return response
 
#????????????
def Berkeley_output(request,value):
    #?????????
    count = 0
    url = f'https://search.books.com.tw/search/query/key/{value}/cat/BKA'
    while True:  #??????????????????
        try:
            browser(url)
            time.sleep(2)
            soup=BeautifulSoup(driver.page_source,'html.parser')
        except:
            pass
        else:
            none_item=soup.find_all('div',class_ = 'none clearfix') #???????????????
            search_results=soup.find_all('div',class_='search_results') #???????????????
            if none_item!=[] or search_results!=[]:
                if none_item != []:
                    msg = f'??????????????? {value} ?????????'
                break
            else:
                print(f"{value} ????????? ??????????????????")
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
    berkely_bs = dict(list(berkely_bs.items())[:6]) #??????6????????????
    if request.user.is_authenticated:
        for href in berkely_bs:
            exist_records = collection_table.objects.filter(uName=request.user, book_url=href, book_Name=berkely_bs[href]['name'], book_Price=int(berkely_bs[href]['price']), lib="0")
            if exist_records:
                berkely_bs[href]['fav'] = "????????????"
            else:
                berkely_bs[href]['fav'] = "????????????"
    else:
        for href in berkely_bs:
            berkely_bs[href]['fav'] = "????????????"
    print(f'{value} ?????????????????????')
    
    #?????????????????????
    driver.get('https://book.tpml.edu.tw/webpac/webpacIndex.jsp')
    keyword = driver.find_element(By.CSS_SELECTOR,'#search_inputS')
    keyword.send_keys(value)
    keyword.submit()
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    dVC = soup.find_all('div',id='detailViewDetailContent')
    len_detail = len(dVC)
    tptp = "tptp"
    if len_detail != 0:
        print(f'{value} ???????????????????????????')
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

        tp1_fav = "????????????"
        if request.user.is_authenticated:
            exist_records_tp1 = collection_table.objects.filter(uName=request.user, book_Name=TC_BookName, lib="1", book_Info=marc)
            if exist_records_tp1:
                tp1_fav = "????????????"
        

    else:
        iframe = driver.find_elements(By.TAG_NAME,"iframe")[0]
        driver.switch_to.frame(iframe)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        totalnum = int(soup.find('em',id='totalpage').text)
        if totalnum > 0:
            if totalnum > 3:
                totalnum = 3
            html_num = [fm + 1 for fm in range(totalnum)]
            print(f'{value} ????????????{totalnum}?????????')
            hrefs = ['https://book.tpml.edu.tw/webpac/' + i.a['href'] for i in soup.find_all('h4')]
            last = []
            for fm in range(totalnum):
                addup = []
                try:
                    driver.get(hrefs[fm])
                    addup.append(hrefs[fm])
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
            if request.user.is_authenticated:
                for i in range(len(last)):
                    exist_records_tp2 = collection_table.objects.filter(uName=request.user, book_Name=last[i][1], lib="1", book_Info=last[i][2])
                    print(exist_records_tp2)
                    if exist_records_tp2:
                        
                        last[i].append((i+1)*1000)
                        last[i].append("????????????")
                    else:
                        
                        last[i].append((i+1)*1000)
                        last[i].append("????????????")
            else:
                for i in range(len(last)):
                    last[i].append((i+1)*500)
                    last[i].append("????????????")
        elif totalnum == 0:
            msg2 = f'??????????????? {value} ?????????'


        


    #?????????????????????
    driver.get(f'https://webpac.tphcc.gov.tw/webpac/search.cfm?m=ss&k0={value}&t0=k&c0=and')
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    no_data_len = len(soup.find_all('p',string='?????????????????????'))
    if no_data_len == 0:
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="wrap"]/div[3]/div/div[2]/div[2]/div[1]/div[2]/span'))) # wait totalnum
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        page_display = soup.find('div',class_='page-display').text
        p_f = page_display.find('???') + 1
        page_display = page_display[p_f:]
        p_l = page_display.find('???')
        page_display = int(page_display[:p_l])
        if page_display > 3:
            page_display = 3
        NT_last = []
        print(f'{value} ???????????????{page_display}???')
        
        hrefs = ['https://webpac.tphcc.gov.tw/webpac/' + h3.parent['href'] for h3 in soup.find_all('h3')]
        for display in range(page_display):
            try:
                addup = []
                driver.get(hrefs[display])
                addup.append(hrefs[display])
                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="wrap"]/div[3]/div/div[2]/div[3]/div[2]/div[2]'))) # wait detail
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                name = soup.find('div',{'class':'right'})
                NT_BookName = name.h2.text.strip(space) #??????
                addup.append(NT_BookName)
                information = soup.find('div',{'class':'detail simple'})
                allP = information.findAll('p')
                paragraphs = []
                for p in allP:
                    p_list=[i.strip(space) for i in p.text.split(chr(32)+chr(65306)+chr(32))]
                    paragraphs.append(tuple(p_list))
                addup.append(paragraphs)


                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="wrap"]/div[3]/div/div[2]/div[5]/div/table/tbody'))) #wait ????????????
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
        if request.user.is_authenticated:

            for i in range(len(NT_last)):
                exist_records_ntp = collection_table.objects.filter(uName=request.user, book_Name=NT_last[i][1], lib="2", book_url=NT_last[i][0])
                
                if exist_records_ntp:
                    NT_last[i].append((i+1)*10000)
                    NT_last[i].append("????????????")
                else:
                    NT_last[i].append((i+1)*10000)
                    NT_last[i].append("????????????")
        else:
            for i in range(len(NT_last)):
                NT_last[i].append((i+1)*50)
                NT_last[i].append("????????????")
    elif no_data_len > 0:
        msg3 = f'??????????????? {value} ?????????'

    
    return render(request, "Berkeley_output.html", locals())



#????????????
def Berkeley_post(request):
    if request.COOKIES != None:
        if 'searchword' in request.COOKIES:
            bytes_list = ast.literal_eval(request.COOKIES['searchword'])
            bytes_list = [byte.decode() for byte in bytes_list]

    if request.method =='POST':
        keyword = request.POST['keyword'].strip(space)
        print('?????????',keyword)
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


# ????????????
def sign_up(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  #???????????????????????????
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


#??????
def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  #?????????????????????
    context = {
        'form': form
    }
    return render(request, 'login.html', context)

# ??????
def log_out(request):
    logout(request)
    return redirect('/') #???????????????????????????

def collection(request):
    exist_records_bkl = collection_table.objects.filter(uName=request.user, lib="0")

    exist_records_tp = collection_table.objects.filter(uName=request.user, lib="1")

    exist_records_ntp = collection_table.objects.filter(uName=request.user, lib="2")
    return render(request, 'collection.html', locals())

def add_fav_ajax(request):
    data = {'success': False}

    if request.method=='POST':
        # ?????????
        if request.POST.get("flag") == "bkl":
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
                    'book_Name': bookname, 'book_Price': int(bookprice), 'book_Info': bookinfo, 'lib': "0"}
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
                    print("????????????")
        # ?????????
        elif request.POST.get("flag") == "tp":
            bookname = request.POST.get("bookname")
            bookurl = request.POST.get("bookurl")
            bookinfo = request.POST.get("bookinfo")
            


            if not request.user.is_authenticated:
                data['success'] = -1
                return JsonResponse(data)

            exist_records = collection_table.objects.filter(uName=request.user, book_Info=bookinfo, book_Name=bookname, lib="1")

            if exist_records:
                exist_records.delete()
                data['success'] = -2

            else:
                datas = {'uName': request.user, 'book_url': bookurl, 
                    'book_Name': bookname, 'book_Price': 0, 'book_Info': bookinfo, 'lib': "1"}
                form = collection_tableModelForm(datas)
                form.uName = request.user
                form.book_url = bookurl
                form.book_Name = bookname
                form.book_Price = 0
                form.book_Info = bookinfo
                form.lib = "1"
                if form.is_valid():
                    form.save()
                    data['success'] = True
                else:
                    print(form.errors)
                    print("????????????")


        # ?????????
        elif request.POST.get("flag") == "ntp":
            bookname = request.POST.get("bookname")
            bookurl = request.POST.get("bookurl")
            bookinfo = request.POST.get("bookinfo")
            print("bookinfo",bookinfo)
            print("type(bookinfo)", type(bookinfo))


            if not request.user.is_authenticated:
                data['success'] = -1
                return JsonResponse(data)

            exist_records = collection_table.objects.filter(uName=request.user, book_url=bookurl, book_Name=bookname, lib="2")

            if exist_records:
                exist_records.delete()
                data['success'] = -2

            else:
                datas = {'uName': request.user, 'book_url': bookurl, 
                    'book_Name': bookname, 'book_Price': 0, 'book_Info': bookinfo, 'lib': "2"}
                form = collection_tableModelForm(datas)
                form.uName = request.user
                form.book_url = bookurl
                form.book_Name = bookname
                form.book_Price = 0
                form.book_Info = bookinfo
                form.lib = "2"
                if form.is_valid():
                    form.save()
                    data['success'] = True
                else:
                    print(form.errors)
                    print("????????????")

    return JsonResponse(data)





