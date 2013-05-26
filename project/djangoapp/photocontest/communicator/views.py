# Create your views here.
# -*- coding: utf-8 -*-

from photocontest.template_path import register_path, profile_path, myuploads_path #@UnresolvedImport
from photocontest import settings #@UnresolvedImport
import os
import sys

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from models import UserProfile, UploadImage
from forms import RegistrationForm, UploadImageForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms import ValidationError
from django.contrib.auth.decorators import login_required

def register_view (request):
    logout(request)
    message = None
    if request.method == "POST":
        user = None
        form = RegistrationForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                cd = form.cleaned_data
                
                # for optional value
                age = cd['age'] or None
                sex = cd['sex'] or None
                
                user = User.objects.create_user(form.cleaned_username(),
                                            form.cleaned_email(),
                                            form.cleaned_password2()) 
                
                userProfile = UserProfile(
                                          type = cd['type'],                                          
                                          location =cd['location'],
                                          profile_image = cd['profile_image'],
                                          user = user,                                          
                                          age = age,    # optional value
                                          sex = sex,    # optional value
                                          )                
                userProfile.save()

                return HttpResponseRedirect("/")
            else:
                message = str(form.errors)
        except:
            if user:
                user.delete()
            message = str(sys.exc_info()[1])
            
    form = RegistrationForm()
    return render_to_response(register_path, RequestContext(
                request, { "message": message, "form": form } ) )

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required
def profile_view(request):
    try:
        myprofile = request.user.get_profile()
    except:
        raise Http404
     
    return render_to_response(profile_path, RequestContext(
                        request, {'profile':myprofile}) )
        
@login_required
def upload_view(request):
    message = None
    if request.method == "POST":
        try:
            form = UploadImageForm(request.POST, request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                uploadImage = UploadImage(image = cd['image'],
                                                     category = cd['category'], 
                                                     title = cd['title'],
                                                     user = request.user)
                
                uploadImage.save()
                return HttpResponseRedirect("/")
            else:
                message = str(form.errors)
        except:
            if os.path.exists(os.path.join(settings.MEDIA_ROOT, cd['image'].path)):
                os.remove(os.path.join(settings.MEDIA_ROOT, cd['image'].path))
            message = str(sys.exc_info()[1])
            
    form = UploadImageForm()
    return render_to_response(register_path, RequestContext(
                request, { "message": message, "form": form } ) )

@login_required
def get_my_uploads_view(request):
    try:
        images = UploadImage.objects.filter(user = request.user)
    except:
        message = str(sys.exc_info()[1])        
    
    return render_to_response(myuploads_path, 
                              RequestContext( request, {'images':images }))

def delete_my_upload_view(request):
    return HttpResponse("TO DO delete_my_upload_view")

def reset_my_upload_point_view(request):
    return HttpResponse("TO DO reset_my_image_point_view")

def next_images_view(request):
    return HttpResponse("TO DO next_images_view")

def get_best_images_view(request):
    return HttpResponse("TO DO get_best_images_view")

def main_view(request):
    thisModules = sys.modules["photocontest.communicator.views"]
    viewFuns = [ v for v in dir(thisModules)
                if callable(getattr(thisModules, v)) and v.endswith("_view") and v != "main_view"]
    
    viewFuns.append("login_view")

    "<a href='/%s'>%s</a><br>\n"
    return HttpResponse("".join([
                                "<a href='/%s'>%s</a><br>\n" % ( v[:-5], v[:-5])
                                for v in viewFuns ])
    )
