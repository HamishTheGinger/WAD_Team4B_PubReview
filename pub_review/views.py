from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    context_dict = {}

    # get list of top 5 pubs
    pub_list =  Pub.objects.order_by('-review_score')[:5]
    context_dict['top_pubs_list'] = pub_list

    # get list of recent reviews
    reviews = Review.objects.order_by('-Date')[:10]
    context_dict['recent_reviews_list'] = reviews

    return render(request, 'pub_review/index.html', context= context_dict)

def placeholder(request):
    context_dict = {}
    return render(request, 'pub_review/placeholder.html', context=context_dict)

def search(request):
    context_dict = {}
    return render(request, 'pub_review/index.html', context= context_dict)

def pubs(request):
    return HttpResponse("<h1>To be made</h1>")

def add_pub(request):
    return HttpResponse("<h1>To be made</h1>")

def show_pub(request):
    return HttpResponse("<h1>To be made</h1>")

def edit_pub(request):
    return HttpResponse("<h1>To be made</h1>")

def show_reviews(request):
    return HttpResponse("<h1>To be made</h1>")

def show_review(request):
    return HttpResponse("<h1>To be made</h1>")

def list_questions(request):
    return HttpResponse("<h1>To be made</h1>")

def show_question(request):
    return HttpResponse("<h1>To be made</h1>")

def add_answer(request):
    return HttpResponse("<h1>To be made</h1>")

def edit_answer(request):
    return HttpResponse("<h1>To be made</h1>")

def user_profile(request):
    return HttpResponse("<h1>To be made</h1>")

def user_profile_reviews(request):
    return HttpResponse("<h1>To be made</h1>")

def edit_user_profile(request):
    return HttpResponse("<h1>To be made</h1>")

def user_login(request):
    return HttpResponse("<h1>To be made</h1>")

def register(request):
    return HttpResponse("<h1>To be made</h1>")

def user_logout(request):
    return HttpResponse("<h1>To be made</h1>")
