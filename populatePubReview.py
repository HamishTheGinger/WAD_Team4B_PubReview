import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team4b_pub_review.settings')

import django
django.setup()

from pub_review.models import UserProfile, Answer, Question, Pub, FavoritePubs, Review
from datetime import timezone

def populate():
    """
    Creates 7 Users, 6 pubs, 2 questions and 3 answers.
    There are 6 pub owners, Users 1-6 and 1 regular user, user 7
    Pub 1 has 2 questions.
    Question 1 has 1 answer, Question 2 has 2.
    """


    # create profile dictionaries
    users_data = [
        {'username': 'User1','first_name': 'John', 'last_name': 'Doe', 'password': 'password1', 'email': 'user1@example.com'},
        {'username': 'User2','first_name': 'Jane', 'last_name': 'Smith', 'password': 'password2', 'email': 'user2@example.com'},
        {'username': 'User3','first_name': 'Bob', 'last_name': 'Johnson', 'password': 'password3', 'email': 'user3@example.com'},
        {'username': 'User4','first_name': 'Alice', 'last_name': 'Brown', 'password': 'password4', 'email': 'user4@example.com'},
        {'username': 'User5','first_name': 'Charlie', 'last_name': 'Davis', 'password': 'password5', 'email': 'user5@example.com'},
        {'username': 'User6','first_name': 'Eva', 'last_name': 'Wilson', 'password': 'password6', 'email': 'user6@example.com'},
        {'username': 'User7','first_name': 'Frank', 'last_name': 'Miller', 'password': 'password7', 'email': 'user7@example.com'},
    ]
    # create pub dictionaries
    pubs_data = [
        {'owner': users_data[0], 'pub_name': 'Pub 1', 'city': 'Glasgow', 'street_name': '70 Arygle Street', 'postcode': 'G2 8AG'},
        {'owner': users_data[1], 'pub_name': 'Pub 2', 'city': 'Glasgow', 'street_name': '56 Arygle Street', 'postcode': 'G2 8AG'},
        {'owner': users_data[2], 'pub_name': 'Pub 3', 'city': 'Glasgow', 'street_name': 'University Ave', 'postcode': 'G12 8SP'},
        {'owner': users_data[3], 'pub_name': 'Pub 4', 'city': 'Glasgow', 'street_name': '17 Vinicombe St', 'postcode': 'G12 8SJ'},
        {'owner': users_data[4], 'pub_name': 'Pub 5', 'city': 'Glasgow', 'street_name': 'Byres Rd, Glasgow G12 8QX', 'postcode': ''},
        {'owner': users_data[5], 'pub_name': 'Pub 6', 'city': 'Glasgow', 'street_name': '106 Arygle Street', 'postcode': ''},
    ]

    # create Question dictionaries
    questions_data = [
        {'author': users_data[1], 'pub': pubs_data[0], 'subject': 'Question 1', 'content': 'Content of Question 1'},
        {'author': users_data[6], 'pub': pubs_data[0], 'subject': 'Question 2', 'content': 'Content of Question 2'},
    ]

    # create Answer dictionaries
    answers_data = [
        {'author': users_data[2], 'question': questions_data[0], 'pub': pubs_data[0], 'content': 'Answer to Question 1'},
        {'author': users_data[3], 'question': questions_data[1], 'pub': pubs_data[0], 'content': 'Answer 1 to Question 2'},
        {'author': users_data[4], 'question': questions_data[1], 'pub': pubs_data[0], 'content': 'Answer 2 to Question 2'},
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
        create_pub(**pub_data)

    for question_data in questions_data:
        create_question(**question_data)

    for answer_data in answers_data:
        create_answer(**answer_data)

    for review_data in reviews_data:
        create_review(**review_data)

    # Populate Database tables
    def create_user_profile(first_name, last_name, sex, age, nationality):
        # don't know how to set User model variables
        profile = UserProfile.objects.get_or_create(firstName=first_name, lastName=last_name, sex=sex, age=age, nationality=nationality)[0]
        profile.save()
        return profile

    def create_pub(owner, pub_name, city, street_name, postcode):
        pub = Pub.objects.get_or_create(owner=owner, pubName=pub_name, city=city, streetName=street_name, postcode=postcode)[0]
        pub.save()
        return pub

    def create_question(author, pub, subject, content):
        question = Question.objects.get_or_create(author=author, pub=pub, subject=subject, content=content, create_date=timezone.now())[0]
        question.save()
        return question

    def create_answer(author, question, pub, content):
        answer = Answer.objects.get_or_create(author=author, question=question, pub=pub, content=content, create_date=timezone.now())[0]
        answer.save()
        return answer

    def create_review(author, pub, subject, content):
        review = Review.objects.get_or_create(author=author, pub=pub, subject=subject, content=content, create_date=timezone.now())[0]
        review.save()
        return review

# Start execution here!
if __name__ == '__main__':
    print('Starting population script...')
    populate()    

