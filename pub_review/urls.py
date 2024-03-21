from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name= 'pub_review'
urlpatterns = [
    path('',views.index, name ='index'),

    # Question and Answer URLs
    path('questions/',views.list_questions,name="questions"),
    path('question/<int:question_id>/',views.detail, name = 'detail'),
    path('question/create/',views.question_create, name = 'question_create'),
    path('answer/create/<int:question_id>/',views.answer_create, name = 'answer_create'),
    path('question/modify/<int:question_id>/',views.question_modify,name='question_modify'),
    path('question/delete/<int:question_id>/',views.question_delete, name='question_delete'),
    path('answer/modify/<int:answer_id>/',views.answer_modify,name='answer_modify'),
    path('answer/delete/<int:answer_id>/',views.answer_delete, name='answer_delete'),


    # Login URLs
    path('login/',views.user_login, name= 'login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),

    # Pub URLs
    path('search/',views.list_pubs, name='search'),
    path('pub/<int:pub_id>/',views.showPub,name="pubDetail"),
    path('pub/create/',views.pub_create, name= 'pub_create'),
    path('pub/modify/<int:pub_id>/',views.pub_modify,name='pub_modify'),
    path('pub/delete/<int:pub_id>/',views.pub_delete, name='pub_delete'),

    #Review URLs
    path('pub/<int:pub_id>/review/<int:review_id>/',views.showReview, name = 'reviewDetail'),
    path('pub/<int:pub_id>/review/create/',views.review_create, name = 'review_create'),
    path('pub/<int:pub_id>/review/modify/<int:review_id>/',views.review_modify,name='review_modify'),
    path('pub/<int:pub_id>/review/delete/<int:review_id>/',views.review_delete, name='review_delete'),

    #Pub_Question URLs
    path('pub/<int:pub_id>/question/<int:Pub_Question_id>/',views.showPub_Question, name = 'Pub_QuestionDetail'),
    path('pub/<int:pub_id>/question/create/',views.Pub_Question_create, name = 'Pub_Question_create'),
    path('pub/<int:pub_id>/question/<int:Pub_Question_id>/answer/create/',views.Pub_Answer_create, name = 'Pub_Answer_create'),
    path('pub/<int:pub_id>/question/modify/<int:Pub_Question_id>/',views.Pub_Question_modify,name='Pub_Question_modify'),
    path('pub/<int:pub_id>/question/delete/<int:Pub_Question_id>/',views.Pub_Question_delete, name='Pub_Question_delete'),
    path('pub/<int:pub_id>/question/<int:Pub_Question_id>/answer/modify/<int:Pub_Answer_id>/',views.Pub_Answer_modify,name='Pub_Answer_modify'),
    path('pub/<int:pub_id>/question/<int:Pub_Question_id>/answer/delete/<int:Pub_Answer_id>/',views.Pub_Answer_delete, name='Pub_Answer_delete'),

    #User URLs
    path('user/<int:user_id>/',views.showUserProfile,name="userProfile"),
    path('user/modify/<int:user_id>/',views.userProfile_modify,name='user_modify'),
    path('user/delete/<int:user_id>/',views.userProfile_delete, name='user_delete'),

    #Voter URLs
    path('vote/pub/<int:pub_id>/',views.vote_pub,name="vote_pub"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)