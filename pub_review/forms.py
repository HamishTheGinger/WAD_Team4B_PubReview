from django import forms
from pub_review.models import Question, Answer, UserProfile
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
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields =('username','password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture','firstName','lastName','sex','age','nationality',)

        labels = {
            'picture': 'User Image',
            'firstName': 'First Name',
            'lastName': 'Last Name',
            'sex': 'Sex',
            'age': 'Age',
            'nationality': 'Nationality'
        }