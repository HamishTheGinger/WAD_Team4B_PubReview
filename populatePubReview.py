import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team4b_pub_review.settings')

import django
django.setup()

from pub_review.models import User, UserProfile, Answer, Question, Pub, FavoritePubs, Review
from datetime import datetime
from django.utils import timezone
from pytz import utc
from django.core.files import File
from team4b_pub_review import settings



def populate():
    """
    Creates 7 Users, 6 pubs, 2 questions and 3 answers.
    There are 6 pub owners, Users 1-6 and 1 regular user, user 7
    Pub 1 has 2 questions.
    Question 1 has 1 answer, Question 2 has 2.
    """


    # create profile dictionaries
    users_data = [
        {'username': 'John_D_24','first_name': 'John', 'last_name': 'Doe', 'password': 'password1', 'email': 'user1@example.com', 'image':'johnD.jpg'},
        {'username': 'Jane','first_name': 'Jane', 'last_name': 'Smith', 'password': 'password2', 'email': 'user2@example.com', 'image':'JS.jpg'},
        {'username': 'JB','first_name': 'Bob', 'last_name': 'Johnson', 'password': 'password3', 'email': 'user3@example.com', 'image':'JB.jpg'},
        {'username': 'AliceBrown_1973','first_name': 'Alice', 'last_name': 'Brown', 'password': 'password4', 'email': 'user4@example.com', 'image':'AliceB.jpg'},
        {'username': 'Charlie_D','first_name': 'Charlie', 'last_name': 'Davis', 'password': 'password5', 'email': 'user5@example.com', 'image':'CharlieD.jpg'},
        {'username': 'Eva','first_name': 'Eva', 'last_name': 'Wilson', 'password': 'password6', 'email': 'user6@example.com', 'image':'EvaW.jpg'},
        {'username': 'FrankTheMiller','first_name': 'Frank', 'last_name': 'Miller', 'password': 'password7', 'email': 'user7@example.com', 'image':'FrankTM.jpg'},
    ]
    # create pub dictionaries
    pubs_data = [
        {'owner': users_data[0], 'pub_name': 'The Pot Still', 'city': 'Glasgow', 'street_name': '154 Hope St', 'postcode': 'G2 2TH', 'image':'potStill.jpg'},
        {'owner': users_data[1], 'pub_name': 'Moskito', 'city': 'Glasgow', 'street_name': '196 Bath St', 'postcode': 'G2 4HG', 'image':'moskito.jpg'},
        {'owner': users_data[2], 'pub_name': 'Glasgow Univeristy Union', 'city': 'Glasgow', 'street_name': '32 University Ave', 'postcode': 'G12 8LX', 'image':'GUU.jpg'},
        {'owner': users_data[3], 'pub_name': 'Hillhead Book Club', 'city': 'Glasgow', 'street_name': '17 Vinicombe St', 'postcode': 'G12 8SJ', 'image':'HillHeadBC.jpg'},
        {'owner': users_data[4], 'pub_name': 'Òran Mór', 'city': 'Glasgow', 'street_name': 'Byres Rd', 'postcode': 'G12 8QX', 'image':'oranMor.jpg'},
        {'owner': users_data[5], 'pub_name': 'The Alchemist Glasgow', 'city': 'Glasgow', 'street_name': 'Unit 2, George House, George Square', 'postcode': 'G2 1EH', 'image':'alchemist.jpg'},
    ]

    # create Question dictionaries
    questions_data = [
        {'author': users_data[1], 'pub': pubs_data[0], 'subject': 'When is there live music', 'content': 'What dates/times do you have live music in the next month or so'},
        {'author': users_data[6], 'pub': pubs_data[0], 'subject': 'How pricy is it', 'content': 'I want to eat here but I am wondering how expensive the food is, and if it is worth it'},
    ]

    # create Answer dictionaries
    answers_data = [
        {'author': users_data[2], 'question': questions_data[0], 'pub': pubs_data[0], 'content': 'Answer to Question 1'},
        {'author': users_data[3], 'question': questions_data[1], 'pub': pubs_data[0], 'content': 'It is quite expensive, around £15 for a meal, but its good'},
        {'author': users_data[4], 'question': questions_data[1], 'pub': pubs_data[0], 'content': 'Personally I feel it is overpriced for what you are getting, while the food is nice the portions are small'},
    ]

    # create review dictionaries
    reviews_data = [
        {'author': users_data[5], 'pub': pubs_data[5], 'subject': 'Review 1', 'content': 'Content of Review 1'},
        {'author': users_data[6], 'pub': pubs_data[0], 'subject': 'Review 2', 'content': 'Content of Review 2'},
    ]

    for user_data in users_data:
        # TO DO, not sure how to create the user instances
        create_user_profile(**user_data)

    for pub_data in pubs_data:
        ownerInstance = getUserByUsername(pub_data['owner']['username'])

        create_pub(**pub_data, ownerInstance = ownerInstance)

    for question_data in questions_data:
        authorInstance = getUserByUsername(question_data['author']['username'])
        pubInstance = getPubByPubname(question_data['pub']['pub_name'])

        create_question(**question_data, authorInstance= authorInstance, pubInstnace=pubInstance)

    for answer_data in answers_data:
        authorInstance = getUserByUsername(answer_data['author']['username'])
        pubInstance = getPubByPubname(answer_data['pub']['pub_name'])
        questInstance = getQuestionByName(answer_data['question']['subject'])

        create_answer(**answer_data, authorInstance = authorInstance, questionInstance=questInstance, pubInstnace=pubInstance)

    for review_data in reviews_data:
        authorInstance = getUserByUsername(review_data['author']['username'])
        pubInstance = getPubByPubname(review_data['pub']['pub_name'])

        create_review(**review_data, authorInstance = authorInstance, pubInstance=pubInstance)

# Populate Database tables
def create_user_profile(username, password, email, first_name, last_name, image, sex=None, age=None, nationality=None):
    # creating user instance
    userInstance = User.objects.create_user(username=username, password=password, email=email)
    userInstance.save()
    
    # creating user profile 
    profile = UserProfile.objects.get_or_create(user=userInstance, firstName=first_name, lastName=last_name, sex=sex, age=age, nationality=nationality)[0]
    
    # get path to pub image files
    image_dir = os.path.join(settings.STATIC_DIR, "images/population_file_images/profile_images")

    with open(os.path.join(image_dir, image), 'rb') as f:
        # assign image to Profile.picture field
        profile.picture.save(image, File(f)) # image variable is name of picture
    
    profile.save()

    favPub = FavoritePubs.objects.get_or_create(user=profile)
    #favPub.save()

    return profile

def create_pub(owner, pub_name, city, street_name, postcode, image, ownerInstance):
    pub = Pub.objects.get_or_create(owner=ownerInstance, pubName=pub_name, city=city, streetName=street_name, postcode=postcode)[0]

    # get path to pub image files
    image_dir = os.path.join(settings.STATIC_DIR, "images/population_file_images/pub_images")

    with open(os.path.join(image_dir, image), 'rb') as f:
        # assign image to Pub.picture field
        pub.picture.save(image, File(f)) # image variable is name of picture

    pub.save()
    return pub

def create_question(author, pub, subject, content,authorInstance, pubInstnace=None): 
    question = Question.objects.get_or_create(author=authorInstance, pub=pubInstnace, subject=subject, content=content, create_date=datetime(2024, 10, 17, 15, 30,tzinfo=utc))[0]
    question.save()
    return question

def create_answer(author, question, pub, content,authorInstance, questionInstance, pubInstnace=None):
    answer = Answer.objects.get_or_create(author=authorInstance, question=questionInstance, pub=pubInstnace, content=content, create_date=timezone.now())[0]
    answer.save()
    return answer

def create_review(author, pub, subject, content, authorInstance, pubInstance=None):
    review = Review.objects.get_or_create(author=authorInstance, pub=pubInstance, subject=subject, content=content, create_date=timezone.now())[0]
    review.save()
    return review

# helper function, returns user object instance matching username passed
def getUserByUsername(usernameString):
    try:
        userObject = User.objects.get(username = usernameString)
        return userObject
    except:
        return None
    
def getPubByPubname(pubnameString):
    try:
        pubObject = Pub.objects.get(pubName = pubnameString)
        return pubObject
    except:
        return None
    
def getQuestionByName(questionNameString):
    try:
        QuestObject = Question.objects.get(subject = questionNameString)
        return QuestObject
    except:
        return None


# Start execution here!
if __name__ == '__main__':
    print('Starting population script...')
    populate()   
    print('Database Populated')
 