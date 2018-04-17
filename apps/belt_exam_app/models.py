from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
from datetime import datetime
from django.db import IntegrityError


class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        # using a try/except in case of a db IntegrityError due to UNIQUE constraint placed on username field.
        try:
            if len(postData["name"]) < 3:
                errors["name2"] = "Name must be over 3 characters"
            
            if len(postData["username"]) < 3:
                errors["username"] = "Username must be over 3 characters"

            if len(postData["password"]) < 8:
                errors["password"] = "Password must be at least 8 characters"

            if postData["password"] != postData["password2"]:
                errors["password2"] = "Passwords don't match"

        except IntegrityError:
            errors["name"] = "Username must be unique."

        return errors


    def login_validator(self, postData):
        errors = {}

        #check to see if the username entered is correct.
        try:
            data = User.objects.get(username=postData["username"])
            password = data.password
        #This password checker function returns a boolean.
        #The password here is the hashed password stored in the db.
            if not bcrypt.checkpw(postData['password'].encode(), password.encode()) == True:
                errors["password"] = "Password is incorrect"
        except:
             errors["password"] = "Username is incorrect"
        return errors

    def create_trip_validator(self, postData):
        errors = {}
        today = datetime.now()
    
        if len(postData["destination"]) < 2:
            errors["name"] = "Destination must be over 2 characters"

        if len(postData["desc"]) < 3:
            errors["name2"] = "Description must be over 3 characters"

        try:
            start_date_var = postData["start_date"]
            start_date_var2 = datetime.strptime(start_date_var, "%Y-%m-%d") #converting date string to a datetime instance for validation below.

            if today > start_date_var2:
                errors["date"] = "Start date must be a date in the future, not the past, Dr Brown."
        except:
            errors["date2"] ="Please select a start_date"

        try:    
            end_date_var = postData["end_date"]
            end_date_var2 = datetime.strptime(end_date_var, "%Y-%m-%d")

            if start_date_var2 > end_date_var2:
                errors["date3"] = "End date must be after start date."   

            if today > end_date_var2:
                errors["date4"] = "End date must be in the future, not the past."
        except:
              errors["date5"] ="Please select an end_date"

        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()


class Travel(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    desc = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    users = models.ManyToManyField(User, related_name="travels")