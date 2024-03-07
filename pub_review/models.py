from django.db import models

# Create your models here.

class UserTable(models.Model):
    UserId = models.CharField(max_length=8)
    FirstName = models.CharField(max_length=128)
    LastName = models.CharField(max_length=128)
    Sex = models.CharField(max_length=10)
    Age = models.IntegerField(default=0)
    Nationality = models.CharField(max_length=40)

class PubTable(models.Model):
    PubID = models.CharField(max_length=8)
    Pub_Name = models.CharField(max_length=128)
    City = models.CharField(max_length=128)
    Street_Name = models.CharField(max_length=128)
    Postcode = models.CharField(max_length=6)
    UserID = models.ForeignKey(UserTable)

class QuestionTable(models.Model):
    Question_Number = models.CharField(max_length=8)
    Date = models.models.DateField()
    Context = models.CharField(max_length=1000)
    PubID = models.ForeignKey(PubTable)
    UserID = models.ForeignKey(UserTable)

class ReviewTable(models.Model):
    Review_Number = models.CharField(max_length=8)
    Rating = models.IntegerField(default=0)
    Context = models.CharField(max_length=1000)
    Date = models.DateField()
    PubID = models.ForeignKey(PubTable)

class AnswerTable(models.Model):
    Answer_Number = models.CharField(max_length=8)
    Date = models.models.DateField()
    Context = models.CharField(max_length=1000)
    Question_Number = models.ForeignKey(QuestionTable)
    UserID = models.ForeignKey(UserTable)

class Top5_PubTable(models.Model):
    UserID = models.ForeignKey(UserTable)
    PubID = models.ForeignKey(PubTable)

