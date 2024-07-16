from django.shortcuts import render,redirect
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
 

# Create your views here.
@login_required(login_url='/login')
def Mainpage(request):
   return render(request,'Hero.html')

def Homepage(request):
    return render (request,'Hero1.html')

def Signuppage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('pass')
        pass2=request.POST.get('cpass')
        try:    
            if pass1!=pass2:
                #return HttpResponse("Your Pasword and Confirm Passsword Are not same")
                messages.success(request,'Your password and Confirm Password Are not Same')
            else:
                if User.objects.filter(username=uname).first():
                    messages.success(request,'Username is Already Taken')
                    return redirect('signup') 
                if User.objects.filter(email=email).first():
                    messages.success(request,'Email is Already Used')
                    return redirect('signup')
                else:     
                    my_user=User.objects.create_user(uname,email)
                    my_user.set_password(pass1)
                    my_user.save()
                    auth_token=str(uuid.uuid4())
                    profile_obj=Profile.objects.create(user=my_user,auth_token=auth_token)
                    profile_obj.save()
                    send_mail_signup(email,auth_token)
                    return render(request,'token.html')             
        except Exception as e:
            print(e)
    return render (request,'signup.html')        

def Loginpage(request):
    if request.method=='POST':
       username1= request.POST.get('username')
       password1= request.POST.get('pass')
       user_obj=User.objects.filter(username=username1).first()
       if user_obj is None:
           #return HttpResponse('NO user Found Please Sign-In First to continue')
           messages.success(request,'No User Found Please Sign-In First to Continue')
           return redirect('signup')
       
       Profile_obj=Profile.objects.filter(user=user_obj).first()
       
       if not Profile_obj.is_verified:
           #return HttpResponse('Profile Is Not verified Plz verified Your Profile')
           messages.success(request,'Account is not verified Please Verified Your Account') 
           return redirect('signup')
       
       user=authenticate(request,username=username1,password=password1) 
       if user is not None:
           login(request,user)
           return  redirect('home') 
       else:
          messages.success(request,'Wrong Password')
          return redirect('login')   
    return render (request,'login.html')

def Logoutpage(request):
    logout(request)
    return redirect('login')

def Chatpage(request):
    return render (request,'Chat.html')

def Tokenpage(request):
    return render(request,'token.html')

def verify(request , auth_token):
    try:
        profile_obj= Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                 messages.success(request,'Yout Account Has Been Already verified')
                 #return HttpResponse('Your Account has been already verified.')
                 return redirect('/login')
            profile_obj.is_verified= True
            profile_obj.save()
            messages.success(request, 'Your Account has been verified.')
            return redirect('/login')
        else:
            return redirect('')
    except Exception as e:
        print(e) 
        return redirect('')   
            


def send_mail_signup(email,token):
    subject='Your Account Needs to be verified'
    message=f'paste the link to Verify Your Account http://127.0.0.1:8000/verify/{token}'
    email_form = settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject , message, email_form , recipient_list)