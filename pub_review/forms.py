from django import forms
from pub_review.models import Question, Answer, UserProfile,Pub,Review,Pub_Answer,Pub_Question,FavoritePubs
from django.contrib.auth.models import User
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject','content']
        labels ={
            'subject':'Title',
            'content':'Content',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        label ={
            "content": 'Answer',
        }

class UserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(label='Comfirmation',widget=forms.PasswordInput())
    class Meta:
        model = User
        fields =('username','email','password1','password2')
        labels = {
            'username': 'User_name',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirmation',
        }



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture','firstName','lastName','sex','age','nationality',)

        labels = {
            'picture': 'User_Image',
            'firstName': 'First_Name',
            'lastName': 'Last_Name',
            'sex': 'Sex',
            'age': 'Age',
            'nationality': 'Nationality'
        }

class PubProfileForm(forms.ModelForm):
    class Meta:
        model = Pub
        fields = ('pubName','city','streetName','postcode','picture')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['subject','content','picture']

class Pub_QuestionForm(forms.ModelForm):
    class Meta:
        model = Pub_Question
        fields = ['subject','content']
        labels ={
            'subject':'Title',
            'content':'Content',
        }

class Pub_AnswerForm(forms.ModelForm):
    class Meta:
        model = Pub_Answer
        fields = ['content']
        label ={
            "content": 'Answer',
        }

class FavoritePubForm(forms.ModelForm):
    class Meta:
        model = FavoritePubs
        fields = ['pub1','pub2','pub3','pub4','pub5']
