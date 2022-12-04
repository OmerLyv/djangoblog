from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm #Bu klasördeki forms dosyasındaki registerform ve loginform'u dahil et

from django.contrib.auth.models import User   #Djangonun user modelini dahil ettik
from django.contrib.auth import login,authenticate,logout # login => Kayıt ettikten sonra userı login yapmamızı sağlıyor  authenticate => aldığı username ve passworda olup olmadığını sorguluycak

from django.contrib import messages #ekrana mesaj yazdırmak için gerekli modül
from django import forms

def register(request):
    """ Birinci Yöntem
    if request.method == "POST": #POST request olduğunda değerleri db ye kaydeteceğimiz yer çalışıcak formumuzu posttan gelen değerlerle doldurucaz
        form = RegisterForm(request.POST)

        if form.is_valid(): #Bu Post request registerform classındaki clean metodu sağlandığında yani validationlar sağlandığında post yapıcak
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            
            newUser = User(username = username)
            newUser.set_password(password)
            newUser.save()

            login(request,newUser) #Kayıt olduktan sonra sisteme otomatik giriş yapmış oldu
            return redirect("index")
        context = {"form" : form}
        return render(request,"register.html",context)

    else:   #Burası GET request yani sadece sitenin register yerini görmek istiyorlar formu doldurmak istiyorlar ama daha formu db ye göndermedik
        form = RegisterForm() 
        context = {"form" : form}
        return render(request,"register.html",context)
"""
    #iKİNCİ YÖNTEM
    form = RegisterForm(request.POST or None) #Post request gelmezse ()parantez içi boş olucak, yani methodu post mu getmi olduğunu kontrol etmek zorunda kalmıyoruz.
    if form.is_valid(): #Bu Post request registerform classındaki clean metodu sağlandığında yani validationlar sağlandığında post yapıcak
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
                
        newUser = User(username = username)
        newUser.set_password(password)
        newUser.save()

        login(request,newUser) #Kayıt olduktan sonra user sisteme otomatik giriş yapmış oldu
        
        messages.success(request,"Başarıyla Kayıt Oldunuz..")

        return redirect("index") #Kayıt olduktan sonra anasayfaya gidiyor
    context = {"form" : form}
    return render(request,"register.html",context)


def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {"form" : form}

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username,password=password) #db ye bakıyor username ve passwordu eşleşen var mı

        if user is None:
            messages.warning(request,"Kullanıcı Adınız veya Şifreniz Hatalı")
            return render(request,"login.html",context = {"form" : form})

        messages.success(request,"Başarıyla Giriş Yaptınız: {}".format(username) )
        login(request,user)
        return redirect("index")


    return render(request,"login.html",context)

def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla Çıkış Yaptınız")
    return redirect("index")