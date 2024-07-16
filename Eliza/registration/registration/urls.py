"""registration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from eliza1 import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('',views.Mainpage,name='hero'),
    path('signup/',views.Signuppage,name='signup'),
    path('login/',views.Loginpage,name='login'),
    path('home/',views.Homepage,name='home'),
    path('log/',views.Logoutpage,name='logout'),
    path('chat/',views.Chatpage,name='chatpage'),
    path('token/',views.Tokenpage,name='tokenpage'),
    path('verify/<auth_token>',views.verify,name='verify'),
       
]

