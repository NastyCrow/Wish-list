from django.db import models
import datetime
# Create your models here.


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData.get('name')) < 3:
            errors[postData.get(
                'name')] = "The name should be at least 3 characters"
        elif len(postData.get('username')) < 3:
            errors[postData.get(
                'username')] = "The username should be at least 3 characters"
        elif User.objects.filter(username=postData.get('username')):
            errors[postData.get('username')] = "The username is already used"
        elif len(postData.get('password')) < 8:
            errors[postData.get(
                'password')] = "The password should be at least 8 characters"
        elif postData.get('password') != postData.get('password_confirm'):
            errors[postData.get('password')
                   ] = "The password and Confirm PW don't match"   
        elif  len(postData["hired_date"]) < 10:
            errors[postData.get('hired_date')
                   ] = "the Date Hired format is wrong"
        elif datetime.datetime.strptime(postData["hired_date"], '%Y-%m-%d').date() > datetime.datetime.now().date():
            errors[postData.get('hired_date')
                   ] = "the Date Hired should be in the past"
        
        return errors



class ItemManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData.get('item_name')) < 3:
            errors[postData.get('item_name')] ="The item must be at least 3 characters"
        elif Item.objects.filter(name=postData.get('item_name')):
            errors[postData.get('item_name')] = "Item already exist"
        return errors
    
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    hired_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()
    
class Item(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User,related_name="created_items",on_delete=models.CASCADE)
    user_who_wish = models.ManyToManyField(User, related_name="whish_list")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=ItemManager()
