from django.conf.urls.defaults import *
from bookmarks.views import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^', include('firstApp.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^$', main_page),
    (r'^user/(\w+)/$', user_page),
    (r'^login/$', "django.contrib.auth.views.login"),
    (r'^logout/$', logout_page),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': "site_media" }),
    (r'^register/$', register_page),
)

# site
root_site = "/"
sites = {
            "admin" : root_site + "admin/",
            "user": root_site + "user/",
            "login": root_site + "login/",
            "logout": root_site + "logout/",
            "site+media": root_site + "site_media/",
            "register": root_site + "register/",           
}

templates = {
             "root": "main_page.html",
             "user": "user_page.html",
             "login": "registration/login.html",
             "register": "registration/register.html",
             }
