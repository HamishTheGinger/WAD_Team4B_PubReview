from django.urls import path
from pub_review import views

app_name = "pub_reviews"

urlpatterns = [
    path('',views.index,name="index"),

    # Pub URLs
    path('pubs/',views.pubs,name="pubs"),
    path('pubs/add_pub/',views.add_pubs,name="add_pubs"),
    path('pubs/<slug:pub_name_slug>/',views.show_pub,name="pub_page"),
    path('pubs/<slug:pub_name_slug>/edit/',views.edit_pub,name="edit_pub_page"),

    # Review URLs
    path('pubs/<slug:pub_name_slug>/reviews/',views.show_reviews,name="show_reviews"),
    path('pubs/<slug:pub_name_slug>/reviews/<int:review_id>',views.show_review,name="review_page"),

    # Question URLs
    path('questions/',views.list_questions,name="list_questions"),
    path('questions/<int:question_id>/',views.show_question,name="show_question"),
    path('questions/<int:question_id>/add_answer/',views.add_answer,name="add_answer"),
    path('questions/<int:question_id/<int:answer_id>/edit/',views.edit_answer,name="edit_answer"),

    # Profile URLs
    path('profile/<int:user_id>/',views.user_profile,name="show_profile"),
    path('profile/<int:user_id>/reviews/',views.user_profile_reviews,name="show_profile_reviews"),
    path('profile/<int:user_id>/edit/',views.edit_user_profile,name="edit_profile"),

    # Login/Signup
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'), 
    path('logout/', views.user_logout, name='logout'),
]
