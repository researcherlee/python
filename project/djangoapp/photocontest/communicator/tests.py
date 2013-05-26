"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from django.contrib.auth.models import User
from models import UserProfile

from test import registration
from test.registration import RegisterTest
from test.login import LoginTest
import models

__test__ = {
            "registration": registration,
            "model_profile": models.UserProfile,
            
            
}

