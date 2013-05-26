# Create your views here.
# -*- coding: utf-8 -*-

from django.http import *
from django.template.loader import *
from django.template.context import *
from django.contrib.auth.models import *
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.template import RequestContext
from forms import RegistrationForm
import bookmarks_proj.urls
from django import forms
import sys

def register_page (request):
    message = None
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        try:
            if form.is_valid():
                user = User.objects.create_user(form.cleaned_username(),
                                            form.cleaned_email(),
                                            form.cleaned_password2())                
                return HttpResponseRedirect(bookmarks_proj.urls.root_site)
            else:
                message = str(form.errors)
        except forms.ValidationError:
            message = str(sys.exc_info()[1])
            
    form = RegistrationForm()
    return render_to_response(bookmarks_proj.urls.templates["register"], RequestContext(
	request, { "message": message, "form": form } ) )

def main_page(request):
#    template = get_template("main_page.html")
#    variables = Context({
#                         "head_title": "장고|북마크",
#                         "page_title": "장고 북마크에 오신 것을 환영합니다.",
#                         "page_body": "여기에 북마크를 저장하고 공유할 수 있습니다!"
#    })
    
#    return render_to_response("main_page.html", {"user": request.user})
    return render_to_response("main_page.html", RequestContext(request))
#    
#    output = template.render(variables)
   
#    return HttpResponse(output)


def user_page(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404("사용자를 찾을 수 없습니다.")
    
    bookmarks = user.bookmark_set.all()
    return render_to_response("user_page.html", RequestContext(request, {"username": username, "bookmarks":bookmarks}))
    
    template = get_template("user_page.html")
    
    variables = Context({
                         "username": username,
                         "bookmarks": bookmarks
                         })
    output = template.render(variables)
    return HttpResponse(output)
    
def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/")
