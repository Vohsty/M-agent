from django.db import models
import datetime as dt
from django.contrib.auth.models import User
import os
import binascii
import random

# Create your models here.

from django.contrib.auth.models import AbstractUser
# from django.contrib.auth import get_user_model
# User = get_user_model()

class User(AbstractUser):
    
    def __str__(self):
        return self.first_name

    def save_user(self):
        self.save()

class Tenant(models.Model):
    user=models.OneToOneField(User, verbose_name=(""), on_delete=models.CASCADE, related_name="tenant")
    # tenant_hash=models.CharField(max_length=255,unique=True)
    first_name = models.CharField(max_length =30)
    last_name = models.CharField(max_length =30)
    email = models.EmailField(unique=True)
    id_number= models.CharField(max_length =30,unique=True)
    phone_number = models.CharField(max_length = 10,unique=True)
    pin = models.CharField(max_length = 5,unique=True,null=True)
    image = models.ImageField(upload_to='images/')
    post_date = models.DateTimeField(auto_now_add=True)
    gender_choices = [('M', 'Male'), ('F', 'Female')]
    tenant = models.BooleanField(default=True)
    gender = models.CharField(
        choices=gender_choices,
        max_length=1,
        default=None,
        null=True)
    house_name = models.OneToOneField('House', on_delete=models.DO_NOTHING, null=True,related_name="occupant")
    my_house = models.CharField(max_length = 10,unique=True,null=True)
    def __str__(self):
        return self.first_name

    def create_pin(self):
        pin= random.randint(10000,99999)
        if Tenant.objects.filter(pin=pin).first():
            self.create_pin()
        self.pin="{pin}".format(pin=pin)
        self.save()
        return pin
    def generate_otp_password(self):
        otp=os.urandom(4).hex()
        self.user.set_password(otp)
        self.user.save()
        return otp

    


    # def generate_key(self):
    #     key=binascii.hexlify(os.urandom(32)).decode()
    #     card= SecurityCards(key=key)
    #     card.save()
    #     self.security_card=card
    #     self.save()
    #     return key
        

    def save_tenant(self):
        self.save()
    
    @classmethod
    def user_profile(cls,id):
        profile = User.objects.get(id=id)
        return profile

class Landlord(models.Model):
    user=models.OneToOneField(User, verbose_name=(""), on_delete=models.CASCADE, related_name="landlord")
    id_number= models.CharField(max_length =30)
    phone_number = models.CharField(max_length = 10)
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return self.user.username

    def save_landlord(self):
        self.save()
    
class Building(models.Model):
    owner = models.ForeignKey(Landlord,on_delete=models.CASCADE,related_name="buildings")
    building_name = models.CharField(max_length =30)
    building_location = models.CharField(max_length =30)
    street = models.CharField(max_length =30)
    plot_number= models.CharField(max_length =30)

    def __str__(self):
        return self.building_name

    def save_building(self):
        self.save()

class House(models.Model):
    house_choice = [('B', 'B-sitter'), ('1Br', 'One Bedroom'), ('2Br', 'Two Bedroom'),('3Br', 'Three Bedroom')]
    house_type = models.CharField(choices=house_choice,max_length=3,default=None,null=True)
    house_floor = models.CharField(max_length=5,null=True)
    name = models.CharField(max_length=10)
    rent=models.PositiveIntegerField(default=1)
    vacant = models.BooleanField(default=True)
    building = models.ForeignKey('Building', on_delete=models.CASCADE,null=True,related_name="building_houses")
    

    def __str__(self):
        return self.name

    def save_house(self):
        self.save()

class SecurityCards(models.Model):
    is_working=models.BooleanField(default=False)
    key=models.CharField(max_length=255,unique=True)
    tenant= models.OneToOneField(Tenant, on_delete=models.CASCADE,related_name="security_card")


    def save_key(self):
        self.save()




class Transactions(models.Model):
    tenant=models.ForeignKey(Tenant, related_name="payments",on_delete=models.DO_NOTHING,null=True)
    house=models.ForeignKey(House,related_name="rents",on_delete=models.DO_NOTHING,null=True)
    amount=models.PositiveIntegerField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    short_code=models.CharField(max_length=255,null=True)
    meta=models.TextField(null=True)

    class Meta:
        verbose_name_plural="Transactions"

    
    def __str__(self):
        return "Transaction:{id}".format(id=self.id)
   