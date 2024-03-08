from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name= 'pub_review'
urlpatterns = [
    path('',views.index, name = 'index'),

    # Question URLs
    path('questions/',views.list_questions,name="questions"),
    path('<int:question_id>/',views.detail, name = 'detail'),
    path('question/create/',views.question_create, name = 'question_create'),
    path('answer/create/<int:question_id>/',views.answer_create, name = 'answer_create'),

    #Login URLs
    path('login/',views.user_login, name= 'login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),

]