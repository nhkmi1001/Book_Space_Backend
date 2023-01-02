from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User
from django.test.client import encode_multipart, BOUNDARY, MULTIPART_CONTENT
import tempfile

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
    @classmethod
    def setUpTestData(self):
        self.user_success_data = {"email": "test@test.com", "username": "test", "password":"test1234"}
        self.user_fail_data = {"email": "test", "username": "test", "password": "test1234"}
        self.user = User.objects.create_user("test@test.com", "test", "test1234")
        self.user.is_active = True
        
    def setUp(self):
        self.access_token = self.client.post(reverse("user:token_obtain_pair_view"), self.user_success_data).data["access"]
        self.refresh_token = self.client.post(reverse("user:token_obtain_pair_view"), self.user_success_data).data["refresh"]
    #로그인 성공
    def test_access_token_login_success(self):
        response = self.client.post(reverse("user:token_obtain_pair_view"), self.user_success_data)
        self.assertEqual(response.status_code, 200)
    
    #로그인 실패
    def test_access_token_login_fail(self):
        response = self.client.post(reverse("user:token_obtain_pair_view"), self.user_fail_data)
        self.assertEqual(response.status_code, 400)

class MypageViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(self):
         self.user_data = {"email": "test@test.com", "username": "test", "password":"test1234"}
         self.user1 = User.objects.create_user("test@test.com", "test", "test1234")
         self.user2 = User.objects.create_user("test1@test.com", "test1", "test12345")
    
    def setUp(self):
        self.access_token = self.client.post(reverse("user:token_obtain_pair_view"), self.user_data).data["access"]
    
    #개인 프로필
    def test_user_profile_success(self):
        response = self.client.get(
            path=reverse("user:mypage_view", kwargs={"user_id": "1"}), 
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}", 
            )
        self.assertEqual(response.status_code, 200)
    
    #프로필 수정 성공
    def test_user_update_success(self):
        response = self.client.put(
            path = reverse("user:mypage_view", kwargs={"user_id" : "1"}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}", 
            data = {"username": "testtt123", "password":"testtt1234", "passwordcheck":"testtt1234"}
        )
        self.assertEqual(response.status_code, 200)
    
    #프로필 수정 username 만
    def test_user_update_username(self):
        response = self.client.put(
            path = reverse("user:mypage_view", kwargs={"user_id" : "1"}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}", 
            data = {"username": "testtt123", "password": "", "password": ""}
        )
        self.assertEqual(response.status_code, 200)
        
    #프로필 수정 password 만
    def test_user_update_password(self):
        response = self.client.put(
            path = reverse("user:mypage_view", kwargs={"user_id" : "1"}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}", 
            data = {"username": "", "password": "testtt123", "passwordcheck": "testtt123"}
        )
        self.assertEqual(response.status_code, 200)    
        
    #프로필 수정 실패(username, password 둘다 빈칸)
    def test_user_update_two_blank_fail(self):
        response = self.client.put(
            path = reverse("user:mypage_view", kwargs={"user_id" : "1"}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}", 
            data = {"username": "", "password": ""}
        )
        self.assertEqual(response.status_code, 400)

    #프로필 수정 실패(유저네임 중복)
    def test_user_update_username_unique_fail(self):
        response = self.client.put(
            path = reverse("user:mypage_view", kwargs={"user_id" : "1"}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}", 
            data = {"username": "test1", "password": ""}
        )
        self.assertEqual(response.status_code, 400)        

    #사용자 탈퇴
    def test_user_delete_success(self):
        response = self.client.delete(
          path=reverse("user:mypage_view", kwargs={"user_id": "1"}),
          HTTP_AUTHORIZATION = f"Bearer {self.access_token}",   
        )
        self.assertEqual(response.status_code, 202)

class MypageImageViewCaseTest(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.user_data = {"email": "test@test.com", "username": "test", "password":"test1234"}
        self.user = User.objects.create_user("test@test.com", "test", "test1234")
    
    def setUp(self):
        self.access_token = self.client.post(reverse("user:token_obtain_pair_view"), self.user_data).data["access"]
    #프로필 이미지 변경 성공
    def test_user_update_image_success(self):
        image = tempfile.NamedTemporaryFile(suffix="fb-thankful.png").name
        response = self.client.put(
            path = reverse("user:mypage_image_view", kwargs={"user_id": "1"}),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token}",
            content_type=MULTIPART_CONTENT,
            data=encode_multipart(
                data={
                    "profile_image": image,
                },
                boundary=BOUNDARY,
            ),
        )
        self.assertEqual(response.status_code, 200)

class UserChoiceBookViewCaseTest(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.user_data = {"email": "test@test.com", "username": "test", "password":"test1234"}
        self.user = User.objects.create_user("test@test.com", "test", "test1234")
    
    def setUp(self):
        self.access_token = self.client.post(reverse("user:token_obtain_pair_view"), self.user_data).data["access"]
    #사용자가 취향인 책을 선택하고 저장 성공
    def test_select_book_save_success(self):
        response = self.client.post(
            path=reverse("user:user_choice_book_view"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data={
                "choice":[1,2,3]
            }
        )
        self.assertEqual(response.status_code, 200)

class LikeArticlesViewCaseTest(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.user_data = {"email": "test@test.com", "username": "test", "password":"test1234"}
        self.user = User.objects.create_user("test@test.com", "test", "test1234")
    
    def setUp(self):
        self.access_token = self.client.post(reverse("user:token_obtain_pair_view"), self.user_data).data["access"]
    
    #게시글 좋아요
    def test_article_like_success(self):
        response = self.client.get(
            path=reverse("user:like_articles_view", kwargs={"user_id":"1"}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)
