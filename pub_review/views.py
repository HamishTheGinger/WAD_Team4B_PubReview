from django.shortcuts import render

# Create your views here.
def index(request):
    context_dict = {}
    return render(request, 'pub_review/index.html', context= context_dict)

def placeholder(request):
    context_dict = {}
    return render(request, 'pub_review/placeholder.html', context=context_dict)