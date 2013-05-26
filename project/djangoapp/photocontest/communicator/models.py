
import os, random, string
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# global setting information
PROFILE_IMAGE_WIDTH = 100
PROFILE_IMAGE_HEIGHT = 300
USER_PROFILE_UPLOAD_ROOT = "upload_images/"

def get_profile_image_path(instance, filename):
    chars = string.letters + string.digits
    name = "".join(random.sample(chars, 2))
    ext = os.path.splitext(filename)[1]
    return "%s%s/profile%s%s" % (USER_PROFILE_UPLOAD_ROOT, instance.user.id, name, ext)

def get_upload_image_path(instance, filename):
    chars = string.letters + string.digits
    name = "".join(random.sample(chars, 8))
    ext = os.path.splitext(filename)[1]
    return "%s%s/%s%s" % (USER_PROFILE_UPLOAD_ROOT, instance.user.id, name, ext)

class Category(models.Model):
    name = models.CharField(max_length = 20)
    
    def __unicode__(self):
        return u"%s" % self.name
    
class UploadImage(models.Model):
    '''
    It expresses uploaded image by users
    '''
    image = models.ImageField(upload_to=get_upload_image_path)
    title = models.CharField(max_length =20)
    uploaded = models.DateTimeField(auto_now = True)
    
    total_rated_count = models.IntegerField(default = 0)
    total_rated_point = models.IntegerField(default = 0)
    average_rated = models.IntegerField(default = 0)
    viewed_count = models.IntegerField(default = 0)

    user = models.ForeignKey(User)    
    category = models.ForeignKey(Category)
    
    def __unicode__(self):
        return u"%s %s" % (self.title, self.uploaded.strftime("%Y/%m/%d"))

class UserProfile(models.Model):
    '''
    It is an extended class for User.
    
    >>> User.objects.get(username = "test")
    Traceback (most recent call last):
        ...
    DoesNotExist: User matching query does not exist.
    >>> User.objects.create_user(username = "test", email = "tester@test.com", password="123")
    <User: test>
    >>> user = User.objects.get(username="test")
    >>> u = UserProfile(user = user)
    >>> u.save()
    >>> u.max_succesive_hits
    0
    >>> u.current_succesive_hits
    0
    >>> u.fair_point
    500
    >>> u.age
    >>> u.sex
    >>> u.location
    >>> u.profile_image
    <ImageFieldFile: None>
    >>> u.total_giving_point
    0
    >>> u.total_giving_count
    0
    >>> u.average_uptatined_point
    0
    >>> user.delete()
    '''
    SEX_CHOICES = (
            ('M', 'Male'),
            ('F', 'Female'),
            )

    TYPE_CHOICES = (
             ('P', 'Paid User'),
             ('F', 'Free User'),
             )

    max_succesive_hits = models.IntegerField(default=0)
    current_succesive_hits = models.IntegerField(default = 0)

    fair_point = models.IntegerField(default = 500)
    type = models.CharField(max_length=1, choices = TYPE_CHOICES, default="P")
    age = models.IntegerField( null=True, blank=True)
    sex = models.CharField(max_length =1, choices = SEX_CHOICES,  null=True, blank=True)
    location = models.CharField(max_length = 20,  null=True, blank=True)    
    #profile_image = models.ImageField(upload_to="images/profiles", height_field = PROFILE_IMAGE_HEIGHT, width_field = PROFILE_IMAGE_WIDTH, null=True, blank=True)
    profile_image = models.ImageField(upload_to=get_profile_image_path, null=True, blank=True)

    total_giving_point = models.IntegerField(default = 0)
    total_giving_count = models.IntegerField(default = 0)
    average_giving_point = models.IntegerField(default = 0)

    total_uptained_point = models.IntegerField(default = 0)
    total_uptained_count = models.IntegerField(default = 0)
    average_uptained_point = models.IntegerField(default = 0)

    joined = models.DateTimeField(auto_now = True)

    user = models.ForeignKey(User, unique= True)

    def __unicode__(self):
        return u"%s %s " % (self.user.username, self.joined.strftime("%Y/%m/%d"))
