"""first URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    ### ccClub
    path('delete_cookie/<str:key>',views.delete_cookie),
    path('Berkeley_output/<str:value>',views.Berkeley_output),
    path('Berkeley_post/',views.Berkeley_post),
    path('',views.Berkeley_post),
    path('register/', views.sign_up, name='Register'),
    path('login/', views.sign_in, name='Login'),
    path('logout/', views.log_out, name='Logout'),
    path('collection/', views.collection, name='Collection'),

]