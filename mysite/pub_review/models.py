from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Question(models.Model):
    subject = models.CharField(max_length =200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()


class UserProfile(models.Model):
    # These are commented out as they are stored in the django models.User table
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images',blank= True)
    firstName = models.CharField(max_length=128)
    lastName = models.CharField(max_length=128)
    sex = models.CharField(max_length=10,blank= True)
    age = models.IntegerField(default=0,blank= True)
    nationality = models.CharField(max_length=40,blank= True)

    def __str__(self):
        return self.user.username

class Pub(models.Model):
    Pub_Name = models.CharField(max_length=128)
    City = models.CharField(max_length=128)
    Street_Name = models.CharField(max_length=128)
    Postcode = models.CharField(max_length=7) # 7 chars long, longest postcode is "AB123YZ" format
    UserID = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.Pub_Name


