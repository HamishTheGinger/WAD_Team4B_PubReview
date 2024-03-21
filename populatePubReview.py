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
    Creates 7 Users, 6 pubs, each user has 2 reviews, 2 questions and 2 answers.
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
        {'owner': users_data[3], 'pub_name': 'Hillhead Book Club', 'city': 'Glasgow', 'street_name': '17 Vinicombe St', 'postcode': 'G12 8SJ', 'image':'HillheadBC.jpg'},
        {'owner': users_data[4], 'pub_name': 'Òran Mór', 'city': 'Glasgow', 'street_name': 'Byres Rd', 'postcode': 'G12 8QX', 'image':'oranMor.jpg'},
        {'owner': users_data[5], 'pub_name': 'The Alchemist Glasgow', 'city': 'Glasgow', 'street_name': 'Unit 2, George House, George Square', 'postcode': 'G2 1EH', 'image':'alchemist.jpg'},
    ]

    # create Question dictionaries
    questions_data = [
        {'author': users_data[5], 'pub': pubs_data[0], 'subject': 'Happy hour?', 'content': 'Does The Pot Still have a happy hour? If so, what are the timings and deals?'},
        {'author': users_data[4], 'pub': pubs_data[1], 'subject': 'Live Music Schedule', 'content': 'Does Moskito have live music on weekends? Looking for a place with good music.'},
        {'author': users_data[0], 'pub': pubs_data[2], 'subject': 'Food Menu', 'content': 'What kind of food does Glasgow University Union serve? Any recommendations?'},
        {'author': users_data[3], 'pub': pubs_data[3], 'subject': 'Book Club Events', 'content': 'Does Hillhead Book Club host any book-related events or readings?'},
        {'author': users_data[1], 'pub': pubs_data[4], 'subject': 'Accessibility', 'content': 'Is Òran Mór wheelchair accessible? Planning to visit with a friend who has mobility issues.'},
        {'author': users_data[1], 'pub': pubs_data[5], 'subject': 'Reservation Policy', 'content': 'Does The Alchemist Glasgow take reservations? Planning a special occasion and want to make sure we can get a table.'},
        {'author': users_data[5], 'pub': pubs_data[0], 'subject': 'Whisky Tasting Events', 'content': 'Does The Pot Still host any whisky tasting events? Would love to learn more about Scotch whisky.'},
        {'author': users_data[6], 'pub': pubs_data[1], 'subject': 'Happy Hour Deals', 'content': 'What are the happy hour deals at Moskito? Looking for a place with good drink specials.'},
        {'author': users_data[3], 'pub': pubs_data[2], 'subject': 'Student Discounts', 'content': 'Does Glasgow University Union offer any discounts for students? Planning to visit with a group of friends on a budget.'},
        {'author': users_data[2], 'pub': pubs_data[3], 'subject': 'Private Events', 'content': 'Is it possible to book a private event at Hillhead Book Club? Interested in hosting a party for a special occasion.'},
        {'author': users_data[3], 'pub': pubs_data[4], 'subject': 'Outdoor Seating', 'content': 'Does Òran Mór have outdoor seating? Hoping to enjoy the nice weather while sipping on a drink.'},
        {'author': users_data[6], 'pub': pubs_data[5], 'subject': 'Signature Cocktails', 'content': 'What are the signature cocktails at The Alchemist Glasgow? Any must-try drinks?'},
        {'author': users_data[4], 'pub': pubs_data[0], 'subject': 'Trivia Nights', 'content': 'Does The Pot Still host trivia nights? Looking for a fun activity to do with friends.'},
        {'author': users_data[2], 'pub': pubs_data[1], 'subject': 'Live Music Genre', 'content': 'What genres of music are typically played at Moskito? Interested in checking out some local bands.'},
        {'author': users_data[0], 'pub': pubs_data[2], 'subject': 'Membership Benefits', 'content': 'What are the benefits of becoming a member of Glasgow University Union? Is it worth signing up?'},
    ]

    # create Answer dictionaries
    answers_data = [
        {'author': users_data[0], 'question': questions_data[0], 'pub': pubs_data[0], 'content': 'Yes, The Pot Still has a happy hour from 5pm to 7pm every weekday. They offer discounts on selected drinks.'},
        {'author': users_data[0], 'question': questions_data[1], 'pub': pubs_data[1], 'content': 'Yes, Moskito often has live music on weekends. Check their website or social media for the schedule.'},
        {'author': users_data[1], 'question': questions_data[2], 'pub': pubs_data[2], 'content': 'Glasgow University Union serves a variety of pub-style food, including burgers, pizzas, and snacks. The nachos are particularly popular.'},
        {'author': users_data[1], 'question': questions_data[3], 'pub': pubs_data[3], 'content': 'Yes, Hillhead Book Club hosts book-related events such as author readings and book club meetings. Check their events calendar for upcoming activities.'},
        {'author': users_data[2], 'question': questions_data[4], 'pub': pubs_data[4], 'content': 'Yes, Òran Mór is wheelchair accessible. There is a ramp at the main entrance for easy access.'},
        {'author': users_data[2], 'question': questions_data[5], 'pub': pubs_data[5], 'content': 'Yes, The Alchemist Glasgow does take reservations. It\'s recommended to book in advance, especially for larger groups or special occasions.'},
        {'author': users_data[3], 'question': questions_data[6], 'pub': pubs_data[0], 'content': 'Yes, The Pot Still occasionally hosts whisky tasting events. Follow them on social media for announcements about upcoming events.'},
        {'author': users_data[3], 'question': questions_data[7], 'pub': pubs_data[1], 'content': 'Moskito offers various drink specials during happy hour, including discounts on cocktails, beer, and wine.'},
        {'author': users_data[4], 'question': questions_data[8], 'pub': pubs_data[2], 'content': 'Yes, Glasgow University Union offers discounts for students on food and drinks. It\'s definitely worth taking advantage of if you\'re a student.'},
        {'author': users_data[4], 'question': questions_data[9], 'pub': pubs_data[3], 'content': 'Yes, Hillhead Book Club has space available for private events. Contact their events team for more information on booking.'},
        {'author': users_data[5], 'question': questions_data[10], 'pub': pubs_data[4], 'content': 'Yes, Òran Mór has outdoor seating available in their beer garden. It\'s a lovely spot to enjoy a drink on a sunny day.'},
        {'author': users_data[5], 'question': questions_data[11], 'pub': pubs_data[5], 'content': 'The Alchemist Glasgow is known for its innovative cocktails. Some popular choices include the Smokey Old Fashioned and the Colour Changing Negroni.'},
        {'author': users_data[6], 'question': questions_data[12], 'pub': pubs_data[0], 'content': 'Yes, The Pot Still occasionally hosts trivia nights. Keep an eye on their events calendar for details.'},
        {'author': users_data[6], 'question': questions_data[13], 'pub': pubs_data[1], 'content': 'Moskito features a variety of music genres, including indie, rock, and electronic. There\'s something for everyone.'},
        {'author': users_data[6], 'question': questions_data[14], 'pub': pubs_data[2], 'content': 'Membership at Glasgow University Union comes with perks like discounts on drinks, access to exclusive events, and voting rights in union elections.'},
    ]

    # create review dictionaries
    reviews_data = [        
        {'author': users_data[0], 'pub': pubs_data[1], 'subject': 'Great Atmosphere', 'content': 'Moskito has a great atmosphere with dim lighting and cozy seating. Perfect for a night out.', 'image':"review3moskito.jpg"},
        {'author': users_data[0], 'pub': pubs_data[2], 'subject': 'Fun Nights Out', 'content': 'It is always buzzing with activity. Whether it is a themed party or karaoke night, there is always something fun happening.'},
        {'author': users_data[1], 'pub': pubs_data[3], 'subject': 'Quirky Decor', 'content': 'The decor at Hillhead Book Club is quirky and eclectic, with bookshelves lining the walls and mismatched furniture. Love the unique vibe.'},
        {'author': users_data[1], 'pub': pubs_data[4], 'subject': 'Beautiful Venue', 'content': 'Òran Mór is housed in a beautiful building with stunning architecture. The interior is just as impressive, with high ceilings and ornate details.', 'image':"review1OranMor.jpg"},
        {'author': users_data[2], 'pub': pubs_data[5], 'subject': 'Impeccable Service', 'content': 'The service at The Alchemist Glasgow is impeccable. The staff is attentive and knowledgeable, making for a memorable dining experience.'},
        {'author': users_data[2], 'pub': pubs_data[0], 'subject': 'Authentic Pub', 'content': 'The Pot Still feels like stepping into a traditional Scottish pub. From the whisky selection to the decor, everything exudes authenticity.'},
        {'author': users_data[3], 'pub': pubs_data[1], 'subject': 'Creative Cocktails', 'content': 'The cocktails at Moskito are both creative and delicious. The mixologists really know their craft.'},
        {'author': users_data[3], 'pub': pubs_data[2], 'subject': 'Nostalgic Vibes', 'content': 'Glasgow University Union brings back fond memories of my university days. It is a nostalgic trip every time I visit.'},
        {'author': users_data[4], 'pub': pubs_data[3], 'subject': 'Hidden Gem', 'content': 'Hillhead Book Club is a hidden gem in Glasgow\'s West End. It is a bit off the beaten path, but well worth seeking out.', 'image':"review4HillheadBC.jpg"},
        {'author': users_data[4], 'pub': pubs_data[4], 'subject': 'Scenic Location', 'content': 'The location at Òran Mór offers scenic views of the bustling street below. It is a prime spot for people-watching.', 'image':"review2OranMor.jpg"},
        {'author': users_data[5], 'pub': pubs_data[5], 'subject': 'Innovative Drinks', 'content': 'The Alchemist Glasgow is known for its innovative drinks that push the boundaries of mixology. Each cocktail is a work of art.'},
        {'author': users_data[5], 'pub': pubs_data[0], 'subject': 'Whisky Paradise', 'content': 'The Pot Still is a whisky lover\'s paradise. With shelves lined with bottles from floor to ceiling, there is something for every palate.', 'image':"review5thePotStill.jpg"},
        {'author': users_data[6], 'pub': pubs_data[1], 'subject': 'Lively Ambiance', 'content': 'Moskito has a lively ambiance with upbeat music and friendly patrons. It is always a good time here.'},
        {'author': users_data[6], 'pub': pubs_data[2], 'subject': 'Student Hangout', 'content': 'Glasgow University Union is the ultimate student hangout. Whether you are grabbing a pint between classes or attending a society event, it is a hub of activity.'},
        {'author': users_data[6], 'pub': pubs_data[3], 'subject': 'Cozy Spot', 'content': 'Hillhead Book Club\'s cozy atmosphere makes it the perfect spot to escape the cold Glasgow weather. Curl up with a book and a hot drink for the ultimate comfort.'}
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

def create_review(author, pub, subject, content, authorInstance, pubInstance=None, image=""):
    review = Review.objects.get_or_create(author=authorInstance, pub=pubInstance, subject=subject, content=content, create_date=timezone.now())[0]

    if image != "":
        # get path to pub image files
        image_dir = os.path.join(settings.STATIC_DIR, "images/population_file_images/review_images")

        with open(os.path.join(image_dir, image), 'rb') as f:
            # assign image to Pub.picture field
            review.picture.save(image, File(f)) # image variable is name of picture

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
 