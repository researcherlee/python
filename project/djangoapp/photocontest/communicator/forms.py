'''
Created on 2009. 10. 15.

'''
from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from models import UserProfile, UploadImage

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ["title", "image", "category"]

    
class RegistrationForm(forms.Form):
        
    username = forms.CharField(label = "User name" , max_length=30)
    email = forms.EmailField()
    password1 = forms.CharField(label = "Password", widget = forms.PasswordInput())
    password2 = forms.CharField(label = "Password(Verification)", widget = forms.PasswordInput())
    
    type = forms.ChoiceField(choices = UserProfile.TYPE_CHOICES)
    age = forms.IntegerField(max_value=200, min_value=10, required=False)
    sex = forms.ChoiceField(choices = UserProfile.SEX_CHOICES, required=False)
    location = forms.CharField(max_length = 20,  required=False)    
    profile_image = forms.ImageField(required=False)
  
    def cleaned_type(self):
        data = self.cleaned_data["type"]        
        if data and data not in [ a[0] for a in UserProfile.TYPE_CHOICES ]:
            raise forms.ValidationError("Type Incorrect.")
        return data
        
    def cleaned_sex(self):
        data = self.cleaned_data["sex"]        
        if data and data not in [ a[0] for a in UserProfile.SEX_CHOICES ]:
            raise forms.ValidationError("Sex Incorrect.")
        return data

  
    def cleaned_username(self):
        username = self.cleaned_data["username"]
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError("Username should be the sqeucence of alphabet, number and '_'")
        
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
        raise forms.ValidationError("Email already exists.")
    
