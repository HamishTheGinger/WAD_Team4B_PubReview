from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from pub_review.models import PubTable, ReviewTable, QuestionTable, AnswerTable, UserTable, Top5_PubTable
from pub_review.forms import AddPubForm, UserForm, UserProfileForm, EditPubForm, AddAnswerForm, EditAnswerFrom, ReviewForm, EditReviewForm

# Create your views here.
def index(request):
    context_dict = {}

    # get list of top 5 pubs
    pub_list =  PubTable.objects.order_by('-review_score')[:5]
    context_dict['top_pubs_list'] = pub_list

    # get list of recent reviews
    reviews = ReviewTable.objects.order_by('-Date')[:10]
    context_dict['recent_reviews_list'] = reviews

    return render(request, 'pub_review/index.html', context= context_dict)

def placeholder(request):
    context_dict = {}
    return render(request, 'pub_review/placeholder.html', context=context_dict)

def search(request):
    context_dict = {}
    return render(request, 'pub_review/index.html', context= context_dict)

def pubs(request):
    """
    This view does not have the functionality 
    for the pubs to be ordered in any way, instead the pubs must be
    ordered using the QuerySet passed out
    """
    
    context_dict = {}
    
    # get list of all pubs to be displayed
    pubs = PubTable.objects.all()
    context_dict["pub_List"] = pubs

    return render(request, 'pub_review/pubs.html',context_dict)


@login_required     # this should maybe be admin only?
def add_pub(request):
    # make call to AddPub form
    form = AddPubForm()
    
    if request.method == "POST":
        form = AddPubForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            #TO-DO
            return redirect()               # Not sure if this should become a redirect to the newly created pub page?
        else:
            print(form.errors)

    return render(request, 'pub_review/pubs/add_pub.html', {'form':form})

def show_pub(request):
    return HttpResponse("<h1>To be made</h1>")

@login_required
def edit_pub(request):
        # make call to AddPub form
    form = EditPubForm()
    
    if request.method == "POST":
        form = EditPubForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            #TO-DO
            return redirect()               # redirect to newly edited pub page.
        else:
            print(form.errors)

    return HttpResponse("<h1>To be made</h1>")

def show_reviews(request):
    return HttpResponse("<h1>To be made</h1>")

@login_required # maybe can be done by hiding like button, instead of this way.
def like_review_view(request):
    # This will be JS function to add the like button functionality to the 
    
    return HttpResponse("<h1>To be made</h1>")

def show_review(request):
    return HttpResponse("<h1>To be made</h1>")

def list_questions(request):
    return HttpResponse("<h1>To be made</h1>")

def show_question(request):
    return HttpResponse("<h1>To be made</h1>")

@login_required
def add_answer(request):
    return HttpResponse("<h1>To be made</h1>")

@login_required
def edit_answer(request):
    return HttpResponse("<h1>To be made</h1>")

def user_profile(request):
    #qeury Top5pub filter by UserID, get list of pub IDs, use those to reference PubTable for list of pubs.
    context_dict = {}

    # Here I cannot figure out how to get the top 5 pubs for any given user using just the request, as UserID here is not tied to anything other than URL.
    top5 = Top5_PubTable.objects.filter(userID = )
    return HttpResponse("<h1>To be made</h1>")

def user_profile_reviews(request):
    return HttpResponse("<h1>To be made</h1>")

@login_required
def edit_user_profile(request):
    return HttpResponse("<h1>To be made</h1>")

def user_login(request):
    if request.method == "POST":
        # POST request, try to log user in using credentials sent
        username = request.POST.get("username")
        password = request.POST.get("password")

        #use django built in functionality to verify login details
        user = authenticate(username, password)

        # if user instance was found, log user in
        if user:
            if user.is_active:
                # log user in
                login(request, user)
                return redirect(reverse('pub_review:index'))
            else:
                return HttpResponse("Your Pub Reviews account is disabled!")
        else:
            return HttpResponse("The login details provided were incorrect. ")
    # likely a GET request, serve login page to user
    else:
        return render(request, "pub_review/login.html")

def register(request):
    #TO-DO finish configuring the user forms, this is not suitable for our use.
    registered = False

    if request.method == 'POST':
        # most of this sourced from tango with django online tutorial
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'pub_review/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))