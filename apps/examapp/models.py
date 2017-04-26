from __future__ import unicode_literals

from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re, datetime
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register(self, data):
        errors= []
        if len(data['f_name'])<3:
            errors.append("First Name must be at least 3 characters")
        if not data['f_name'].isalpha():
            errors.append("First Name must letters")
        if len(data['l_name'])<3:
            errors.append("Last Name must be at least 3 characters")
        if not data['l_name'].isalpha():
            errors.append("Last Name must letters")
        if len(data['password'])<8:
            errors.append("Password must be at least 8 characters")
        if not data['password']==data['con_pw']:
            errors.append("Password and confirm password doesn't match")
        if len(data['email'])<1:
            errors.append("Email cannot be blank!")
        elif not EMAIL_REGEX.match(data['email']):
            errors.append("email format is wrong!")
        else:
            pass
        try:
            User.objects.get(email = data['email'])
            errors.append("email already exixst!")
        except:
            pass
        if len(errors) == 0:
            user = User.objects.create(first_name = data['f_name'], last_name = data['l_name'],email = data['email'], password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()))
            return {'user':user,"error":None}
        else:
            return{'user':None,"error":errors}
    def login(self, data):
        errors= []
        try:
            dbemail=User.objects.get(email = data['email'])
            # print dbemail
            # print dbemail.password
            # print bcrypt.hashpw(data['password'].encode('utf-8'), dbemail.password.encode('utf-8'))
            # print User.objects.get(email = data['email'])
            # print "*"*50
            if bcrypt.hashpw(data['password'].encode('utf-8'), dbemail.password.encode('utf-8')) == dbemail.password.encode('utf-8'):
                # print "*"*50
                return {'user':dbemail,"error":None}
            else:
                errors.append("email password doesn't match!")
                return{'user':None,"error":errors}
        except:
            errors.append("email doesn't exist!")
            return{'user':None,"error":errors}

class TripManager(models.Manager):
    def addtrip(self,data):
        errors= []
        if data['destination']=="":
            errors.append("destination can not be empty!")
        if data['plan']=="":
            errors.append("description can not be empty!")
        if data['start_date'] == "":
            errors.append("Start date can not be empty!")
        elif datetime.datetime.strptime(data['start_date'], '%Y-%m-%d') < datetime.datetime.now():
			errors.append("Start date may not be in the past!!")
        if data['end_date'] == "":
            errors.append("End date can not be empty!")
        elif datetime.datetime.strptime(data['end_date'], '%Y-%m-%d') < datetime.datetime.strptime(data['start_date'], '%Y-%m-%d'):
            print "2"*50
            errors.append("End date should not be before start date!!")
            print errors
        if len(errors) == 0:
            trip = Trip(plan_user = data['plan_user'],destination = data['destination'],start_date = data['start_date'], end_date = data['end_date'], plan = data['plan'])
            trip.save()
            user = data['user']
            user.tripusers.add(trip)
            return{
                "trip":trip,
                "errors":None,
            }
        else:
            print errors
            return{
                "trip":None,
                "errors":errors,
            }

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=145)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
class Trip(models.Model):
    user = models.ManyToManyField(User, related_name="tripusers")
    plan_user = models.ForeignKey(User,related_name="planusers",null=True)
    joinbycurr = models.BooleanField(default=False)
    destination = models.CharField(max_length=45)
    start_date = models.DateField(auto_now = False)
    end_date = models.DateField(auto_now = False)
    plan = models.TextField(max_length=500)
    objects = TripManager()
