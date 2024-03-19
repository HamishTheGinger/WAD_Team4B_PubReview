from django.test import TestCase


import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Question
from django.urls import reverse
from pub_review.models import User, UserProfile, Answer, Question, Pub, FavoritePubs, Review


# Create your tests here.

def create_user(username):
    return User.objects.create_user(username=username, password="123")

def create_pub(pubname, owner):
    return Pub.objects.create(owner=owner, pubName=pubname, city="Glasgow",streetName="Hope",postcode="G3")

def create_review(title, content, user, pub):
    return Review.objects.create(author=user, pub=pub, subject=title, content=content, create_date=timezone.now())

def create_question(title, content, user, pub=None):
    return Question.objects.create(subject=title, content=content, create_date=timezone.now(), author=user, pub=pub)

def create_profile(user, first_name=None, surname=None, age=None, gender=None):
    user =  UserProfile.objects.create(user=user, firstName=first_name, lastName=surname, sex=gender, age=age)

    FavoritePubs.objects.create(user=user)

    return user

class IndexViewTests(TestCase):

    def test_index_blank(self):
        response = self.client.get(reverse('pub_review:index'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['top5_pubs'], [])
        self.assertQuerysetEqual(response.context['recent_reviews'], [])



    def test_index_single_pub(self):
        owner = create_user("Dave")
        create_pub("White Horse",owner)
        response = self.client.get(reverse('pub_review:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "White Horse")
        self.assertQuerysetEqual(response.context['top5_pubs'], ["<Pub: White Horse>"])
        self.assertQuerysetEqual(response.context['recent_reviews'], [])


    def test_index_single_review(self):
        owner = create_user("Dave")
        pub = create_pub("White Horse",owner)
        user = create_user("Sandra")
        create_review("Amazing Food","ghahfkhkahjfh",user,pub)      
        response = self.client.get(reverse('pub_review:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Amazing Food")
        self.assertQuerysetEqual(response.context['recent_reviews'], ["<Review: Amazing Food>"])


    def test_index_reviews_and_pubs(self):
        owner = create_user("Dave")
        pub = create_pub("White Horse",owner)
        user = create_user("Sandra")
        create_review("Amazing Food","ghahfkhkahjfh",user,pub)      
        response = self.client.get(reverse('pub_review:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Amazing Food")
        self.assertContains(response, "White Horse")
        self.assertQuerysetEqual(response.context['recent_reviews'], ["<Review: Amazing Food>"])
        self.assertQuerysetEqual(response.context['top5_pubs'], ["<Pub: White Horse>"]) 

class PubViewTest(TestCase):

    def test_pubs_blank_pub(self):
        owner = create_user("Dave")
        pub = create_pub("White Horse",owner)

        response = self.client.get(reverse('pub_review:pubDetail',args=(pub.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "White Horse")
        self.assertContains(response, "Dave")
        self.assertQuerysetEqual(response.context['review_list'], []) 
        self.assertQuerysetEqual(response.context['question_list'], []) 

    def test_pubs_with_single_review(self):
        owner = create_user("Dave")
        pub = create_pub("White Horse",owner)
        user = create_user("Sandra")
        create_review("Amazing Food","Had a great time, and the food was amazing",user,pub)

        response = self.client.get(reverse('pub_review:pubDetail',args=(pub.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "White Horse")
        self.assertContains(response, "Dave")
        self.assertContains(response, "Amazing Food")
        self.assertQuerysetEqual(response.context['review_list'], ["<Review: Amazing Food>"]) 
        self.assertQuerysetEqual(response.context['question_list'], []) 
      
    def test_pubs_with_question(self):
        owner = create_user("Dave")
        pub = create_pub("White Horse",owner)
        user = create_user("Sandra")
        create_question("How pricy is it", "I am wondering how pricy the food is?", user, pub)

        response = self.client.get(reverse('pub_review:pubDetail',args=(pub.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "White Horse")
        self.assertContains(response, "Dave")
        self.assertContains(response, "How pricy is it")
        self.assertQuerysetEqual(response.context['review_list'], []) 
        self.assertQuerysetEqual(response.context['question_list'], ["<Question: How pricy is it>"]) 

    def test_pubs_with_question_and_review(self):
        owner = create_user("Dave")
        pub = create_pub("White Horse",owner)
        user = create_user("Sandra")
        create_question("How pricy is it", "I am wondering how pricy the food is?", user, pub)
        create_review("Amazing Food","Had a great time, and the food was amazing",user,pub)

        response = self.client.get(reverse('pub_review:pubDetail',args=(pub.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "White Horse")
        self.assertContains(response, "Dave")
        self.assertContains(response, "Amazing Food")
        self.assertContains(response, "How pricy is it")

        self.assertQuerysetEqual(response.context['review_list'], ["<Review: Amazing Food>"]) 
        self.assertQuerysetEqual(response.context['question_list'], ["<Question: How pricy is it>"]) 

class QuestionViewTest(TestCase):
    
    def test_questions_blank(self):
        response = self.client.get(reverse('pub_review:questions'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['question_list'], [])



        pass

    def test_questions_single_question(self):
        user = create_user("Sandra")
        create_question("How pricy is it", "I am wondering how pricy the food is?", user)

        response = self.client.get(reverse('pub_review:questions'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How pricy is it")
        self.assertQuerysetEqual(response.context['question_list'], ["<Question: How pricy is it>"])

    def test_questions_multiple_questions(self):
        owner = create_user("Dave")
        pub = create_pub("White Horse",owner)
        user = create_user("Sandra")
        create_question("How pricy is it", "I am wondering how pricy the food is?", user)
        user = create_user("Alex")
        create_question("What pints do you have on tap", "Can you send a list of all the diffrent pints you have avaliable on tap?", user, pub)


        response = self.client.get(reverse('pub_review:questions'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How pricy is it")
        self.assertContains(response, "What pints do you have on tap")

        self.assertQuerysetEqual(response.context['question_list'], ["<Question: What pints do you have on tap>","<Question: How pricy is it>"])

class UserProfileTests(TestCase):
    def test_profile_blank(self):
        user = create_user("Anna")
        create_profile(user)

        response = self.client.get(reverse('pub_review:userProfile',args=(user.id,)))

        self.assertContains(response, "Anna")
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context['review_list'], [])
        self.assertQuerysetEqual(response.context['question_list'], [])
        self.assertQuerysetEqual(response.context['answer_list'], [])


    def test_profile_name_override(self):
        user = create_user("GraceA34")
        create_profile(user, first_name="Grace", surname="Anderson")

        response = self.client.get(reverse('pub_review:userProfile',args=(user.id,)))

        self.assertContains(response, "Grace Anderson")

        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context['review_list'], [])
        self.assertQuerysetEqual(response.context['question_list'], [])
        self.assertQuerysetEqual(response.context['answer_list'], [])

    def test_profile_review(self):
        user = create_user("GraceA34")
        create_profile(user, first_name="Grace", surname="Anderson")

        owner = create_user("Dave")
        pub = create_pub("White Horse",owner)
        create_review("Amazing Food","Amazing Food here",user,pub)   


        response = self.client.get(reverse('pub_review:userProfile',args=(user.id,)))

        self.assertContains(response, "Grace Anderson")

        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context['review_list'], ["<Review: Amazing Food>"])
        self.assertQuerysetEqual(response.context['question_list'], [])
        self.assertQuerysetEqual(response.context['answer_list'], [])

    def test_profile_question(self):
        user = create_user("GraceA34")
        create_profile(user, first_name="Grace", surname="Anderson")

        owner = create_user("Dave")
        pub = create_pub("White Horse",owner)
        create_question("When do you have live music","What dates/times do you have live music in the next month or so",user,pub)   


        response = self.client.get(reverse('pub_review:userProfile',args=(user.id,)))

        self.assertContains(response, "Grace Anderson")

        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context['review_list'], [])
        self.assertQuerysetEqual(response.context['question_list'], ["<Question: When do you have live music>"])
        self.assertQuerysetEqual(response.context['answer_list'], [])


    def test_profile_question_review(self):
        user = create_user("GraceA34")
        create_profile(user, first_name="Grace", surname="Anderson")

        owner = create_user("Dave")
        pub = create_pub("White Horse",owner)
        create_question("When do you have live music","What dates/times do you have live music in the next month or so",user,pub) 
        create_review("Amazing Food","Amazing Food here",user,pub)   
  


        response = self.client.get(reverse('pub_review:userProfile',args=(user.id,)))

        self.assertContains(response, "Grace Anderson")

        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context['review_list'], ["<Review: Amazing Food>"])
        self.assertQuerysetEqual(response.context['question_list'], ["<Question: When do you have live music>"])
        self.assertQuerysetEqual(response.context['answer_list'], [])
