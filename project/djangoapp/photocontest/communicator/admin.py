'''
Created on 2009. 10. 5.
'''

from django.contrib import admin
import models

class UploadImageAdmin(admin.ModelAdmin):
    list_display = ("category", "user", "image")

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_image', "type", "age")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", )

admin.site.register(models.UploadImage, UploadImageAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Category, CategoryAdmin)
