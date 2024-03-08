from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question,Pub,User
from django.utils import timezone
from .forms import QuestionForm, AnswerForm,UserForm,UserProfileForm
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request,'pub_review/home.html')
def list_questions(request):
    page = request.GET.get('page', 1)  # Page
    question_list = Question.objects.order_by('-create_date')

    # Paging
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    return render(request, 'pub_review/Q&A.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pub_review/question_detail.html', context)


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect('pub_review:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pub_review/question_detail.html', context)


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pub_review:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pub_review/question_form.html', context)


from django.shortcuts import render


def signup(request):
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

    return render(request, 'pub_review/signup.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

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

@login_required
def user_logout(request):
# Since we know the user is logged in, we can now just log them out.
    logout(request)
# Take the user back to the homepage.
    return redirect(reverse('pub_review:index'))