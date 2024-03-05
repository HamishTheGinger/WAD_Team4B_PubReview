from django.urls import path
from pub_review import views

app_name='pub_review'

urlpatterns = [
    path('', views.index, name='index'),
    path('placeholder/', views.placeholder, name='placeholder'),
    
]