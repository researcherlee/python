# -!- coding: utf-8 -!-

import django
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

#if django.VERSION[0] > 0 and django.VERSION[1] > 0:
from django import forms
#else:
#    from django import newforms as forms

class RegistrationForm(forms.Form):
    username = forms.CharField(label = "사용자 이름" , max_length=30)
    email = forms.EmailField(label = "이메일")
    password1 = forms.CharField(label = "비밀번호", widget = forms.PasswordInput())
    password2 = forms.CharField(label = "비밀번호 확인", widget = forms.PasswordInput())
    
    def cleaned_username(self):
        username = self.cleaned_data["username"]
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Username should be the sqeucenc of alphabet, number and '_'")
        
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError("Username already exists.")
    
    def cleaned_password2(self):
        if "password1" in self.cleaned_data:
            password1 = self.cleaned_data["password1"]
            password2 = self.cleaned_data["password2"]
            
            if password1 == password2:
                return password2
        raise forms.ValidationError("Password is not matched.")
    
    def cleaned_email(self):
        if "email" in self.cleaned_data:
            email = self.cleaned_data["email"]
            
            try:
                User.objects.get(email=email)
            except ObjectDoesNotExist:
                return email
        raise forms.ValidationError("이미 사용중인 이메일입니다.")
    
