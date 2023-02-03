from django.test import TestCase
# path의 url이 바꿔도 name은 바뀌지 않는 다는 조건에 계속 동일한 테스트 코드를 사용할 수 있다.
# name으로 부터 path를 가지고 오는 방식
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
class UserSignUpAPIViewTestCase(APITestCase):
    # 로그인 성공
    def test_signup(self):
        url = reverse('user:UserView')
        user_data = {
            "email":"test@test.com",
            "username":"test",
            "password":"test123456",
            "passwordcheck":"test123456"
        }
        response = self.client.post(url,user_data)
        self.assertEqual(response.status_code, 201)

class UserLoginAPIViewTestCode(APITestCase):
    def setUp(self):
        self.user_data = {
            "email":"test@test.com",
            "name":"test",
            "password":"test123456"
        }
        self.user = User.objects.create_user('test@test.com','test','test123456')
        print("확인",self.user.is_active) #True로 찍힘
        # self.user.is_active = False
    def test_login(self):
        response = self.client.post(reverse('user:token_obtain_pair'), self.user_data)
        self.assertEqual(response.status_code, 200)
