from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


#선택한 책에 대한 게시글 생성
class CreateArticleBookTestCode(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.user_success_data = {
            "email":"test@test.com",
            "password":"test123456"
        }
        self.user = User.objects.create_user('test@test.com','test123456')
        print("확인2",self.user.is_active)
    def setUp(self):
        self.access_token = self.client.post(reverse('user:token_obtain_pair'), self.user_success_data).data['access']

    def test_fail_if_not_logged_in(self):
        url = reverse('articles:create_article_book')
        article_data = {
            "book_id":"1",
            "image":"",
            "content":"",
            "rating":"",
            "is_private":""

        }
        response = self.client.post(url)
        self.assertEqual(response.status_code, )