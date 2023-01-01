from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User

class UserSignUpTestCase(APITestCase):
    # 회원가입 성공
    def test_signup_success(self):
        user_data = {
            "email": "test@test.com",
            "username": "test",
            "password": "test1234",
            "passwordcheck": "test1234",
        }
        response = self.client.post(reverse("user:user_view"), user_data)
        self.assertEqual(response.status_code, 201)
    
    # 회원가입 실패(이메일 빈칸)   
    def test_signup_email_blank(self):
        url = reverse("user:user_view")
        user_data = {
            "email": "",
            "username": "test",
            "password": "test1234",
            "passwordcheck": "test1234"
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
        
    # 회원가입 실패(이메일 형식)    
    def test_signup_email_invalid(self):
        url = reverse("user:user_view")
        user_data = {
            "email": "test",
            "username": "test",
            "password": "test1234",
            "passwordcheck": "test1234"
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
        
    # 회원가입 실패(이메일 중복)
    def test_signup_email_duplication(self):
        User.objects.create_user("test@test.com", "test", "test1234")
        url = reverse("user:user_view")
        user_data = {
            "email": "test@test.com",
            "username": "test",
            "password": "test1234",
            "passwordcheck": "test1234"
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
    
    # 회원가입 실패(비밀번호 != 비밀번호 확인)
    def test_signup_password_check(self):
        url = reverse("user:user_view")
        user_data = {
            "email": "test@test.com",
            "username": "test",
            "password": "test1234",
            "passwordcheck": "test4321"
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
    
    #회원가입 실패(비밀번호 길이)
    def test_signup_password_length(self):
        url = reverse("user:user_view")
        user_data = {
            "email": "test@test.com",
            "username": "test",
            "password": "t1",
            "passwordcheck": "t1"
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
    
    #회원가입 실패(비밀번호 구성)
    def test_signup_password_validation(self):
        url = reverse("user:user_view")
        user_data = {
            "email": "test@test.com",
            "username": "test",
            "password": "testtest",
            "passwordcheck": "testtest"
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 400)
    
class UserLoginTestCase(APITestCase):
    def setUpTestData(self):
        self.user_success_data = {"email": "test@test.com", "username": "test", "password":"test1234"}
        self.user_fail_data = {"email": "test", "username": "test", "password": "test1234"}
        self.user = User.objects.create_user("test@test.com", "test", "test1234")
        
        
    def setUp(self):
        self.access_token = self.client.post(reverse("user:token_obtain_pair_view"), self.user_success_data).data["access"]
        self.refresh_token = self.client.post(reverse("user:token_obtain_pair_view"), self.user_success_data).data["refresh"]
        