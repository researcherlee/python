'''
Created on 2009. 10. 26.

'''
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from photocontest.communicator.models import UserProfile, UploadImage #@UnresolvedImport
from PIL import Image #@UnresolvedImport

class UploadTest(TestCase):
    
    def testBasicUpload(self):
        user_data = {
                "username":"tester", 
                "email": "tester@test.com",
                "password1": "123",
                "password2": "123",
                "type": "P",
                }    
        
        response = self.client.post("/register/", user_data)
        self.assertEquals(response.status_code, 302)        
        user = User.objects.get(username="tester")
        user_profile = user.get_profile()
        self.assertEquals(user_profile, UserProfile.objects.get(user=user))
        
        self.assertEquals(user_profile.max_succesive_hits, 0)
        self.assertEquals(user_profile.fair_point, 500)
        self.assertEquals(user_profile.average_uptained_point, 0)
        
        # login
        
        # then
        
        Image.init()        
        f = open("communicator/test/data/image.png")
        uploadData = {                
                "profile_image": f 
        }
                
        response = self.client.post("/upload/", uploadData)
        self.assertEquals(response.status_code, 302) 
        user = User.objects.get(username="tester")
        user_profile = user.get_profile()
        
        f = open("communicator/test/data/image.png")
        self.assertEqual(user_profile.profile_image.file.read(), f.read())
        self.assertEquals(user_profile, UserProfile.objects.get(user=user))        
        self.assertEquals(user_profile.max_succesive_hits, 0)
        self.assertEquals(user_profile.fair_point, 500)
        self.assertEquals(user_profile.average_uptained_point, 0)
        
        user.delete()
        self.assertRaises(ObjectDoesNotExist, UserProfile.objects.get, user = user)
