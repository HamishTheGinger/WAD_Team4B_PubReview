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

def create_pub(pubname, owner_name):
    user = create_user(owner_name)
    return Pub.objects.create(owner=user, pubName=pubname, city="Glasgow",streetName="Hope",postcode="G3")

def create_review(title, content, username, pubname, owner):
    user = create_user(username)
    pub = create_pub(pubname, owner)
    return Review.objects.create(author=user, pub=pub, subject=title, content=content, create_date=timezone.now())


class IndexViewTests(TestCase):

    def test_index_blank(self):
        response = self.client.get(reverse('pub_review:index'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['top5_pubs'], [])


    def test_index_single_pub(self):
        create_pub("White Horse","Dave")
        response = self.client.get(reverse('pub_review:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "White Horse")
        self.assertQuerysetEqual(response.context['top5_pubs'], ["<Pub: White Horse>"])

    def test_index_single_review(self):
        create_review("Amazing Food","ghahfkhkahjfh","Sandra","White Horse","Andrew")      
        response = self.client.get(reverse('pub_review:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Amazing Food")
        self.assertQuerysetEqual(response.context['recent_reviews'], ["<Review: Amazing Food>"])


    def test_index_reviews_and_pubs(self):
        create_pub("White Horse","Dave") # fix to pass in the pubobject not name in create review
        create_review("Amazing Food","ghahfkhkahjfh","Sandra","White Horse","Andrew")      
        response = self.client.get(reverse('pub_review:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Amazing Food")#
        self.assertContains(response, "White Horse")
        self.assertQuerysetEqual(response.context['recent_reviews'], ["<Review: Amazing Food>"])
        self.assertQuerysetEqual(response.context['top5_pubs'], ["<Pub: White Horse>"]) 

class PubViewTest(TestCase):

    def test_pubs_blank_pub(self):
        pass

    def test_pubs_with_single_review(self):
        pass

    def test_pubs_with_question(self):
        pass