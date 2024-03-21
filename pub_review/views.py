from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question,Pub,User,Answer,Review,UserProfile,FavoritePubs
from django.utils import timezone
from .forms import QuestionForm, AnswerForm,UserForm,UserProfileForm,PubProfileForm,ReviewForm,FavoritePubForm
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import auth,messages
from django.db.models import Q, Count
# Create your views here.

def index(request):
    top5_pubs = Pub.objects.order_by(Count("-voters"))[:5]
    recent_reviews= Review.objects.order_by('-create_date')[:5]
    context ={'top5_pubs':top5_pubs, 'recent_reviews':recent_reviews}

    # Google Maps Integration
    key = "AIzaSyB5Prlm7hNvW0P2uxPQ71FKdZUsAFHhoUM"


    if top5_pubs.exists():
        context["top_pub"] = top5_pubs[0]
        placeData = [getattr(top5_pubs[0], 'pubName') , getattr(top5_pubs[0], 'streetName'), getattr(top5_pubs[0], 'city')]  # array of strings, containing pub name, street address, city
        for counter in range (0,3):
            #print("Debugging views.py:ln 25 \n placeData [{}] value = {}".format(counter, placeData[counter]))
            placeData[counter] = placeData[counter].replace(" ", "%20") # maps api uses %20 for spaces

        mapURL = "https://www.google.com/maps/embed/v1/place?key={0}&q={1},{2},{3}".format(key,placeData[0],placeData[1],placeData[2])

        context['mapURL'] = mapURL

    return render(request,'pub_review/home.html',context)

def list_questions(request):
    page = request.GET.get('page', 1)  # Page
    kw = request.GET.get('kw','')
    question_list = Question.objects.order_by('-create_date')

    search = request.GET.get("qSearch")

    # If the user has entered a search term, filter based on that term
    if search != None:
     question_list = Question.objects.filter(subject__contains=search)

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    # Paging
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'pub_review/Q&A.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pub_review/question_detail.html', context)

@login_required(login_url='pub_review:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.create_date = timezone.now()
            answer.save()
            return redirect('pub_review:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pub_review/question_detail.html', context)

@login_required(login_url='pub_review:login')
def answer_modify(request,answer_id):
    answer = get_object_or_404(Answer,pk=answer_id)
    if request.user != answer.author:
        messages.error(request,'No Authentication')
        return redirect('pub_review:detail',question_id=answer.question.id)

    if request.method =="POST":
        form = AnswerForm(request.POST,instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pub_review:detail',question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'form' : form}
    return render(request,'pub_review/answer_form.html',context)

@login_required(login_url='pub_review:login')
def answer_delete(request,answer_id):
    answer = get_object_or_404(Answer,pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "No Authentication")
        return redirect('pub_review:detail',question_id=answer.question.id)
    answer.delete()
    return redirect('pub_review:detail',question_id=answer.question.id)

@login_required(login_url='pub_review:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pub_review:questions')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pub_review/question_form.html', context)


from django.shortcuts import render

@login_required(login_url='pub_review:login')
def question_modify(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    if request.user != question.author:
        messages.error(request,'No Authentication')
        return redirect('pub_review:detail',question_id=question.id)

    if request.method =="POST":
        form = QuestionForm(request.POST,instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pub_review:detail',question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form' : form}
    return render(request,'pub_review/question_form.html',context)

@login_required(login_url='pub_review:login')
def question_delete(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    if request.user != question.author:
        messages.error(request, "No Authentication")
        return redirect('pub_review:detail',question_id=question.id)
    question.delete()
    return redirect('pub_review:questions')

def signup(request):
    registered = False
    if request.method == 'POST':
        # most of this sourced from tango with django online tutorial
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            if request.POST['password1'] == request.POST['password2']:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                userProfile = UserProfile.objects.create(user=user)
                FavoritePubs.objects.create(user=userProfile)
                auth.login(request, user)
                user_id = user.id
                return redirect('pub_review:user_modify', user_id=user_id)
            elif  request.POST['password1'] != request.POST['password2']: 
                messages.error(request, 'Passwords do not match')
        else:  
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'pub_review/signup.html', context={'user_form': user_form, 'registered': registered})

def user_login(request):
    if request.method == "POST":
        # POST request, try to log user in using credentials sent
        username = request.POST.get("username")
        password = request.POST.get("password")

        #use django built in functionality to verify login details
        user = authenticate(username=username, password=password)

        # if user instance was found, log user in
        if user:
            if user.is_active:
                # log user in
                login(request, user)
                return redirect(reverse('pub_review:index'))
            else:
                return HttpResponse("Your Pub Reviews account is disabled!")
        else:
            #return HttpResponse("The login details provided were incorrect. ")
            messages.error(request, 'Login Details provided were incorrect')
            return render(request, "pub_review/login.html")

            

    # likely a GET request, serve login page to user
    else:
        return render(request, "pub_review/login.html")

@login_required
def user_logout(request):
# Since we know the user is logged in, we can now just log them out.
    logout(request)
# Take the user back to the homepage.
    return redirect(reverse('pub_review:index'))

def list_pubs(request):
    page = request.GET.get('page', 1)  # Page
    pub_list = Pub.objects.order_by('pubName')

    #search = Seach
    search = request.GET.get("search")

    if search != None:
     pub_list = Pub.objects.filter(pubName__contains=search)

    # Paging
    paginator = Paginator(pub_list, 10)
    page_obj = paginator.get_page(page)

    context = {'pub_list': page_obj}
    return render(request, 'pub_review/search.html', context)

@login_required(login_url='pub_review:login')
def pub_create(request):
    if request.method == 'POST':
        form = PubProfileForm(request.POST, request.FILES) 
        if form.is_valid():
            pub = form.save(commit=False)
            pub.owner = request.user
            pub.save()
            return redirect('pub_review:search')
        else:
            messages.error(request, 'Form Error')
            print(form.errors)

    else:
        form = PubProfileForm()
    context = {'form': form}
    return render(request, 'pub_review/pub_form.html', context={"form":form})

def showPub(request,pub_id):
    pub = get_object_or_404(Pub, pk=pub_id)
    page_review = request.GET.get('page1', 1)
    review = Review.objects.filter(pub=pub)
    review_list = review.order_by('-create_date')
    question = Question.objects.filter(pub=pub)
    question_list = question.order_by('-create_date')
    page_question = request.GET.get('page2',1)
    paginator_review = Paginator(review_list, 10)
    page_obj_review = paginator_review.get_page(page_review)
    paginator_question = Paginator(question_list, 10)
    page_obj_question = paginator_question.get_page(page_question)

    context = {'review_list': page_obj_review, 'page1': page_review, 'pub': pub,'question_list':page_obj_question,'page2':page_question}
    
    # Google Maps Integration
    key = "AIzaSyB5Prlm7hNvW0P2uxPQ71FKdZUsAFHhoUM"
    placeData = [getattr(pub, 'pubName') , getattr(pub, 'streetName'), getattr(pub, 'city')]  # array of strings, containing pub name, street address, city

    for counter in range (0,3):
        #print("Debugging views.py:ln 268 \n placeData [{}] value = {}".format(counter, placeData[counter]))
        placeData[counter] = placeData[counter].replace(" ", "%20") # maps api uses %20 for spaces
    mapURL = "https://www.google.com/maps/embed/v1/place?key={0}&q={1},{2},{3}".format(key,placeData[0],placeData[1],placeData[2])
    context['mapURL'] = mapURL

    return render(request,'pub_review/pub_detail.html',context)

@login_required(login_url='pub_review:login')
def pub_modify(request,pub_id):
    pub = get_object_or_404(Pub, pk=pub_id)
    if request.user != pub.owner:
        messages.error(request,'No Authentication')
        return redirect('pub_review:pubDetail',pub_id=pub.id)

    if request.method =="POST":
        form = PubProfileForm(request.POST, request.FILES, instance=pub)
        if form.is_valid():
            pub = form.save(commit=False)
            pub.save()
            return redirect('pub_review:pubDetail',pub_id=pub.id)
    else:
        form = PubProfileForm(instance=pub)
    context = {'form': form,'pub':pub,}
    return render(request,'pub_review/pub_form.html',context)

@login_required(login_url='pub_review:login')
def pub_delete(request,pub_id):
    pub = get_object_or_404(Pub, pk=pub_id)
    if request.user != pub.owner:
        messages.error(request, "No Authentication")
        return redirect('pub_review:pubDetail',pub_id=pub.id)
    pub.delete()
    return redirect('pub_review:index')


def showReview(request,pub_id,review_id):
    pub = get_object_or_404(Pub, pk=pub_id)
    review = Review.objects.filter(pub=pub, pk=review_id).get()
    context = {'review': review, 'pub':pub,}
    return render(request,'pub_review/review_detail.html',context)

@login_required(login_url='pub_review:login')
def review_create(request, pub_id):
    pub = get_object_or_404(Pub, pk=pub_id)
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.pub = pub
            review.create_date = timezone.now()
            review.save()
            return redirect('pub_review:pubDetail', pub_id=pub.id)
    else:
        form = ReviewForm()
    context = {'form': form,'pub':pub,}
    return render(request, 'pub_review/review_form.html', context)

@login_required(login_url='pub_review:login')
def review_modify(request,pub_id,review_id):
    pub = get_object_or_404(Pub, pk=pub_id)
    review = Review.objects.filter(pub=pub, pk=review_id).get()
    if request.user != review.author:
        messages.error(request,'No Authentication')
        return redirect('pub_review:pubDetail',pub_id=pub.id)

    if request.method =="POST":
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.modify_date = timezone.now()
            review.save()
            return redirect('pub_review:pubDetail',pub_id=pub.id)
    else:
        form = ReviewForm(instance=review)
    context = {'form': form,'pub':pub,}
    return render(request,'pub_review/review_form.html',context)

@login_required(login_url='pub_review:login')
def review_delete(request,pub_id,review_id):
    pub = get_object_or_404(Pub, pk=pub_id)
    review = Review.objects.filter(pub=pub, pk=review_id).get()
    if request.user != review.author:
        messages.error(request, "No Authentication")
        return redirect('pub_review:pubDetail',pub_id=pub.id)
    review.delete()
    return redirect('pub_review:pubDetail',pub_id=pub.id)

@login_required(login_url='pub_review:login')
def Pub_Answer_create(request, pub_id, Pub_Question_id):
    pub = get_object_or_404(Pub, pk=pub_id)
    question = Question.objects.filter(pub=pub, pk=Pub_Question_id).get()
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.pub=pub
            answer.question = question
            answer.create_date = timezone.now()
            answer.save()
            return redirect('pub_review:Pub_QuestionDetail', pub_id=pub.id, Pub_Question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pub_review/Pub_Question_detail.html', context)

@login_required(login_url='pub_review:login')
def Pub_Answer_modify(request,pub_id, Pub_Question_id, Pub_Answer_id):
    pub = get_object_or_404(Pub, pk=pub_id)
    question = Question.objects.filter(pub=pub, pk=Pub_Question_id).get()
    answer = Answer.objects.filter(pub=pub,question=question,pk=Pub_Answer_id).get()
    if request.user != answer.author:
        messages.error(request,'No Authentication')
        return redirect('pub_review:Pub_QuestionDetail', pub_id=pub.id, Pub_Question_id=question.id)

    if request.method =="POST":
        form = AnswerForm(request.POST,instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pub_review:Pub_QuestionDetail', pub_id=pub.id, Pub_Question_id=question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'form' : form}
    return render(request,'pub_review/answer_form.html',context)

@login_required(login_url='pub_review:login')
def Pub_Answer_delete(request,pub_id, Pub_Question_id,Pub_Answer_id):
    pub = get_object_or_404(Pub, pk=pub_id)
    question = Question.objects.filter(pub=pub, pk=Pub_Question_id).get()
    answer = Answer.objects.filter(pub=pub, question=question, pk=Pub_Answer_id).get()
    if request.user != answer.author:
        messages.error(request, "No Authentication")
        return redirect('pub_review:Pub_QuestionDetail', pub_id=pub.id, Pub_Question_id=question.id)
    answer.delete()
    return redirect('pub_review:Pub_QuestionDetail', pub_id=pub.id, Pub_Question_id=question.id)

@login_required(login_url='pub_review:login')
def Pub_Question_create(request,pub_id):
    pub = get_object_or_404(Pub, pk=pub_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.pub=pub
            question.create_date = timezone.now()
            question.save()
            return redirect('pub_review:pubDetail',pub_id=pub.id)
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pub_review/question_form.html', context)



@login_required(login_url='pub_review:login')
def Pub_Question_modify(request,pub_id,Pub_Question_id):
    pub = get_object_or_404(Pub, pk=pub_id)
    question = Question.objects.filter(pub=pub,pk=Pub_Question_id).get()
    if request.user != question.author:
        messages.error(request,'No Authentication')
        return redirect('pub_review:Pub_QuestionDetail',pub_id=pub.id, Pub_Question_id=question.id)

    if request.method =="POST":
        form = QuestionForm(request.POST,instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pub_review:Pub_QuestionDetail',pub_id=pub.id, Pub_Question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form' : form}
    return render(request,'pub_review/question_form.html',context)

@login_required(login_url='pub_review:login')
def Pub_Question_delete(request,pub_id,Pub_Question_id):
    pub = get_object_or_404(Pub, pk=pub_id)
    question = Question.objects.filter(pub=pub, pk=Pub_Question_id).get()
    if request.user != question.author:
        messages.error(request, "No Authentication")
        return redirect('pub_review:Pub_QuestionDetail',pub_id=pub.id, Pub_Question_id=question.id)
    question.delete()
    return redirect('pub_review:pubDetail',pub_id=pub.id)

def showPub_Question(request, pub_id,Pub_Question_id):
    pub = get_object_or_404(Pub, pk=pub_id)
    question = Question.objects.filter(pub=pub, pk=Pub_Question_id).get()
    context = {'question': question,'pub':pub}
    return render(request, 'pub_review/Pub_Question_detail.html',context)

def showUserProfile(request, user_id):
    # Gathering all of the information needed to display the profile
    user = get_object_or_404(User, pk=user_id)
    userProfile = UserProfile.objects.filter(user=user).get()
    top_5_pubs = FavoritePubs.objects.filter(user=userProfile).get()
    review_list = Review.objects.filter(author=user).order_by('-create_date')
    question_list = Question.objects.filter(author=user).order_by('-create_date')
    answer_list = Answer.objects.filter(author=user).order_by('-create_date')
    page_review = request.GET.get('page1', 1)
    page_question = request.GET.get('page2', 1)
    page_answer = request.GET.get('page3', 1)
    paginator_review = Paginator(review_list, 10)
    page_obj_review = paginator_review.get_page(page_review)
    paginator_question = Paginator(question_list, 10)
    page_obj_question = paginator_question.get_page(page_question)
    paginator_answer = Paginator(answer_list, 10)
    page_obj_answer = paginator_answer.get_page(page_answer)
   
    #if the user is authenticated pass the user model to check if the user if viewing their own profile, otherwise don't pass the user model
    if(request.user.is_authenticated): 
        context = {'user':  user, 'review_list':page_obj_review, 'question_list' : page_obj_question, 'answer_list' :page_obj_answer, 'userProfile':userProfile, 'top_5_pubs':top_5_pubs}
    else:
        context = {'review_list':page_obj_review, 'question_list' : page_obj_question, 'answer_list' :page_obj_answer, 'userProfile':userProfile, 'top_5_pubs':top_5_pubs}
    return render(request, 'pub_review/user_profile.html', context)


@login_required(login_url='pub_review:login')
def userProfile_modify(request,user_id):
    user = get_object_or_404(User, pk=user_id)
    userprofile = UserProfile.objects.filter(user=user).get()
    pubs = Pub.objects.order_by('pubName')
    top5_pubs = FavoritePubs.objects.filter(user=userprofile).get()
    userprofile_form = None
    top5_pubs_form = None
    if request.user != user:
        messages.error(request, 'No Authentication')
        return redirect('pub_review:userProfile', user_id=user_id)

    if request.method == "POST":
        userprofile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        top5_pubs_form = FavoritePubForm(request.POST, instance=top5_pubs)
        if userprofile_form.is_valid() and top5_pubs_form.is_valid():
            userprofile_form.save()
            top5_pubs_form.save()
            return redirect('pub_review:userProfile', user_id=user_id)
    else:
        userprofile_form = UserProfileForm(instance=userprofile)
        top5_pubs_form = FavoritePubForm(instance=top5_pubs)
    context = {'userProfile_form': userprofile_form, 'top5_pubs_form': top5_pubs_form, 'pubs': pubs}
    return render(request, 'pub_review/userProfile_form.html', context)

@login_required(login_url='pub_review:login')
def userProfile_delete(request,user_id):
    user = get_object_or_404(User, pk=user_id)
    userProfile = UserProfile.objects.filter(user=user).get()
    if request.user != user:
        messages.error(request, "No Authentication")
        return redirect('pub_review:showUserProfile',user_id=user_id)
    userProfile.delete()
    user.delete()
    return redirect('pub_review:index')

@login_required(login_url='pub_review:login')
def vote_pub(request, pub_id):
    pub = get_object_or_404(Pub, pk=pub_id)
    if request.user == pub.owner:
        messages.error(request, 'The owner is not allowed to recommend own pub')
    else:
        pub.voter.add(request.user)
    return redirect('pub_review:pubDetail', pub_id=pub.id)

