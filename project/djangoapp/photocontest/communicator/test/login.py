''
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.test.client import Client
from photocontest.communicator.models import UserProfile #@UnresolvedImport

class LoginTest(TestCase):
    def testLoginIDPassword(self):
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
        
        # login
        response = self.client.post("/login/", { "username": "tester", "password": "123"})
        self.assertEquals(response.status_code, 302)
        
        response = self.client.post("/login/", { "username": "testerz", "password": "123"})
        self.assertEquals(response.status_code, 200)
        
        
    def testNegative(self):
        pass
        
                                                
        
        
