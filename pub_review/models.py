from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    # These are commented out as they are stored in the django models.User table
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='userProfile_images',blank= True,null=True, default='userProfile_images/default-profile.png')
    firstName = models.CharField(max_length=128,blank= True,null=True)
    lastName = models.CharField(max_length=128,blank=True,null=True)
    sex = models.CharField(max_length=10,blank=True,null=True)
    age = models.CharField(max_length=10,blank=True,null=True)
    nationality = models.CharField(max_length=40,blank=True,null=True)

    def __str__(self):
        return self.user.username

class Pub(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='owner_pub')
    pubName = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    streetName = models.CharField(max_length=128)
    postcode = models.CharField(max_length=7) # 7 chars long, longest postcode is "AB123YZ" format
    picture = models.ImageField(upload_to='pubProfile_images', blank=True,null=True)
    voter = models.ManyToManyField(User,related_name='voter_pub')
    def __str__(self):
        return self.pubName
    
class Question(models.Model):
    subject = models.CharField(max_length =200)
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    pub = models.ForeignKey(Pub,on_delete=models.CASCADE, null=True, blank=True)
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    content = models.TextField()
    pub = models.ForeignKey(Pub,on_delete=models.CASCADE, null=True, blank=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    pub = models.ForeignKey(Pub,on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    picture = models.ImageField(upload_to='review_images', blank=True,null=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject

class FavoritePubs(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    pub1 = models.CharField(max_length=100,null=True, blank=True)
    pub2 = models.CharField(max_length=100,null=True, blank=True)
    pub3 = models.CharField(max_length=100,null=True, blank=True)
    pub4 = models.CharField(max_length=100,null=True, blank=True)
    pub5 = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.user.user.username + "'s top 5"
