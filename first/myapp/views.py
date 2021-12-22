from django.core.checks import messages
from django.shortcuts import redirect, render
# Create your views here.
from django.http import HttpResponse, response
from selenium.webdriver.common import keys
from myapp.models import student
from myapp.form import PostForm, RegisterForm, LoginForm
from django.contrib.auth import authenticate
from django.contrib import auth
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


# Create your views here.
##ccClub
def Chrome():
    global driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(options=chrome_options)

# Chrome()


def browser(path):
    while True:
        try:
            driver.get(path)
            break
        except Exception as e:
            driver.quit()
            Chrome()


def set_cookie(request, key=None, value=None):
    response = HttpResponse(' Cookie save')
    response.set_cookie(key, value)
    return response


def delete_cookie(request,key):
    if key in request.COOKIES:
       response = HttpResponse('Delete Cookie: ' + key)
       response.delete_cookie(key)
       return response
    else:
        return HttpResponse('No cookies: ',key)
 

def Berkeley_output(request,value):
    now = datetime.now()
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
            none_item=soup.find_all('p',string=f'抱歉，找不到您所查詢的 "{value}" 資料') #沒搜尋結果
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
    response = render(request, "Berkeley_output.html", locals())
    utf8 = value.encode('utf-8')
    if 'searchword' in request.COOKIES:
        cookies= request.COOKIES['searchword']
        cookies = ast.literal_eval(cookies)
        if utf8 not in cookies:
            cookies.append(utf8)

        response.set_cookie('searchword',cookies)
    else:
        response.set_cookie('searchword',[utf8])
    return response

def Berkeley_post(request):
    if request.COOKIES != None:
        total = ''
        if 'searchword' in request.COOKIES:
            bytes_list = ast.literal_eval(request.COOKIES['searchword'])
            for byte in bytes_list:
                strcookie = byte.decode()
                total = total +strcookie +', '
        total = total.strip(', ')

    if request.method =='POST':
        keyword = request.POST['keyword']
        print('關鍵字',keyword)
        return redirect(f'/Berkeley_output/{keyword}')
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


