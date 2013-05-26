'''
Created on 2009. 10. 18.

'''
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.test.client import Client
from photocontest.communicator.models import UserProfile #@UnresolvedImport
from django.core.files import File
import os
from PIL import Image #@UnresolvedImport

class RegisterTest(TestCase):
    def testRegFullData(self):
        Image.init()        
        f = open("communicator/test/data/image.jpg")
        data = {
                "username": "tester", 
                "email": "tester@test.com",
                "password1": "123", 
                "password2": "123",
                "type": "P", 
                "age": "20",
                "sex": "M",
                "Location": "Seoul",
                "profile_image": f 
        }
        
        response = self.client.post("/register/", data)
        self.assertEquals(response.status_code, 302)        
        user = User.objects.get(username="tester")
        user_profile = user.get_profile()
        
        f = open("communicator/test/data/image.jpg")
        self.assertEqual(user_profile.profile_image.file.read(), f.read())
        self.assertEquals(user_profile, UserProfile.objects.get(user=user))        
        self.assertEquals(user_profile.max_succesive_hits, 0)
        self.assertEquals(user_profile.fair_point, 500)
        self.assertEquals(user_profile.average_uptained_point, 0)
        
        user.delete()
        self.assertRaises(ObjectDoesNotExist, UserProfile.objects.get, user = user)
        
        
    def testRegIDEmailPassword(self):
        data = {
                "username":"tester", 
                "email": "tester@test.com",
                "password1": "123",
                "password2": "123",
                "type": "P",
                }    
        
        response = self.client.post("/register/", data)
        self.assertEquals(response.status_code, 302)        
        user = User.objects.get(username="tester")
        user_profile = user.get_profile()
        self.assertEquals(user_profile, UserProfile.objects.get(user=user))
        
        self.assertEquals(user_profile.max_succesive_hits, 0)
        self.assertEquals(user_profile.fair_point, 500)
        self.assertEquals(user_profile.average_uptained_point, 0)
        
        user.delete()
        self.assertRaises(ObjectDoesNotExist, UserProfile.objects.get, user = user)
        
        
    def testPRegister(self):
        """
        Case1) Register with ID and Password
        Case2) Register with ID, Password and Age
        Case3) Register with ID, Password and Sex
        Case4) Register with ID, Password and Location
        Case5) Register with All information
        """
        client = Client()
        response = client.get("/register/")
        self.assertEqual(response.status_code, 200)
        
        
    def testNRegisterInvalidID(self):
        """
        Case1) Invalid ID format
        """
        pass
    
    def testNRegisterInvalidPassword(self):
        """
        Case2) Invalid Password format
        """
        pass
    
