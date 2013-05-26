import os.path
from django.conf.urls.defaults import *
from communicator.views import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^photocontest/', include('photocontest.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
     
    # Root
    (r'^$', main_view),
    
    # Command1: register
    (r'^register/$', register_view),
    
    # Command2: login
    (r'^login/$', "django.contrib.auth.views.login"),
    (r'^logout/$', logout_view),
    (r'^profile/$', profile_view),
    
    # Command3: upload
    (r'^upload/$', upload_view),    
    
    # Command4: get_my_uploads / delete_my_upload / reset_my_upload_point
    (r'^get_my_uploads/$', get_my_uploads_view),
    (r'^delete_my_upload/$', delete_my_upload_view),
    (r'^reset_my_upload_point/$', reset_my_upload_point_view),
        
    # Command5: next_images
    (r'^next_images/$', next_images_view),
    
    # Command6: get_best_iamges
    (r'^get_best_images/$', get_best_images_view),
    
)

if settings.DEBUG or not settings.IN_SERVER:
    urlpatterns += patterns('',
                (r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': "media" }),            
    )




