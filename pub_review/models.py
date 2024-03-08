from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserTable(models.Model):
    # This line links UserTable to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    UserId = models.CharField(max_length=8)
    # These are commented out as they are stored in the django models.User table
    #FirstName = models.CharField(max_length=128)
    #LastName = models.CharField(max_length=128)
    Sex = models.CharField(max_length=10)
    Age = models.IntegerField(default=0)
    Nationality = models.CharField(max_length=40)

class PubTable(models.Model):
    PubID = models.CharField(max_length=8)
    Pub_Name = models.CharField(max_length=128)
    City = models.CharField(max_length=128)
    Street_Name = models.CharField(max_length=128)
    Postcode = models.CharField(max_length=7) # 7 chars long, longest postcode is "AB123YZ" format
    UserID = models.ForeignKey(UserTable,null=True,on_delete=models.SET_NULL)

class QuestionTable(models.Model):
    Question_Number = models.CharField(max_length=8)
    Date = models.DateField()
    Context = models.CharField(max_length=1000)
    PubID = models.ForeignKey(PubTable, on_delete=models.CASCADE)
    UserID = models.ForeignKey(UserTable,null=True, on_delete=models.SET_NULL)

class ReviewTable(models.Model):
    Review_Number = models.CharField(max_length=8)
    Rating = models.IntegerField(default=0)
    Context = models.CharField(max_length=1000)
    Date = models.DateField()
    PubID = models.ForeignKey(PubTable, on_delete=models.CASCADE)

class AnswerTable(models.Model):
    Answer_Number = models.CharField(max_length=8)
    Date = models.DateField()
    Context = models.CharField(max_length=1000)
    Question_Number = models.ForeignKey(QuestionTable,on_delete=models.CASCADE)
    UserID = models.ForeignKey(UserTable,null=True,on_delete=models.SET_NULL)

class Top5_PubTable(models.Model):
    UserID = models.ForeignKey(UserTable,on_delete=models.CASCADE)
    PubID = models.ForeignKey(PubTable,on_delete=models.CASCADE)

