from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.



class User(AbstractUser):
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(unique=True,null=True)
    bio = models.TextField(null=True)
    avtar = models.ImageField(null=True,default="avatar.svg")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name
    
    
class Room(models.Model):
    id = models.AutoField(primary_key=True)
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True) 
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    participants = models.ManyToManyField(User,related_name='participants',blank=True) 
    updated = models.DateTimeField(default=datetime.now)
    created = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['-updated','-created']
    
    def __str__(self) -> str:
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE) #on_delete (cascade) is user for when perent is delete then child also delete 
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated','-created']   
        
    def __str__(self) -> str:
        return self.body[:50]
    
    
        