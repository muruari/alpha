from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re

class UserManager(models.Manager):
    def validate(self, postData):
        errors = []

        if len(postData.get('name')) and len(postData.get('username')) < 3:
            is_valid = False
            errors.append('Name and username must have at least 3 characters each. Please try again.')

        if len(User.objects.filter(username = postData.get("username"))) > 0:
            is_valid = False
            errors.append('That username is already taken. Please try again.')

        if not re.search(r'^[a-z" "A-Z]+$', postData.get('name')):
            is_valid = False
            errors.append('Name must be alphabetical characters only. Please try again.')

        if len(postData.get('password')) < 8:
            is_valid = False
            errors.append('Passwords must have at least 8 characters. Please try again.')

        if postData.get('password_confirmation') != postData.get('password'):
            is_valid = False
            errors.append('Passwords do not match. Please try again.')
        return errors

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    
    def __str__(self):
        return "name:{}, username:{}, password:{}, created_at:{}, updated_at:{}".format(self.name, self.username, self.password, self.created_at, self.updated_at)


class TripManager(models.Manager):
    def validate_trip(self, postData):
        errors = []

        if len(postData.get('destination')) and len(postData.get('description')) < 3:
            is_valid = False
            errors.append('Trip destination and description must have at least 3 characters each. Please try again.')

        if postData.get('depart_date') < datetime.today().strftime('%Y-%m-%d'):
            is_valid = False
            errors.append('Trip departure date cannot be in the past. Please enter a valid date.')

        if postData.get('return_date') < postData.get('depart_date'):
            is_valid = False
            errors.append('Trip return date cannot precede trip departure date. Please enter a valid date.')
        return errors


class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)    
    depart_date = models.CharField(max_length = 10)
    return_date = models.CharField(max_length = 10)
    trips = models.ManyToManyField(User, related_name="all_trips")
    created_by = models.ForeignKey(User, related_name="user_trips")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripManager()