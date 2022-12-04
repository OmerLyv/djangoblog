from django import forms
from django.contrib.auth.models import User
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50,label = "Kullanıcı Adı",min_length=4)
    password = forms.CharField(max_length=25,label="Şifre",widget= forms.PasswordInput,min_length=3)
    confirm = forms.CharField(max_length=25,label="Şifrenizi Doğrulayın",widget=forms.PasswordInput,min_length=3)
    
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        user = User.objects.filter(username=username)
        if user.exists():
            raise forms.ValidationError("Kullanıcı adı başka birisi tarafından alınmıştır")
        if (password and confirm) and (password != confirm):     #Şifre eşleştirme ve şifreleri girmişmi kontrol ediyoruz
            raise forms.ValidationError("Şifreleriniz Eşleşmiyor")
        values = {"username": username, "password":password}   #eğer girmişse aldığımız bilgileri sözlüğe aktarıyoruz
        return values

class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Şifre",widget=forms.PasswordInput)