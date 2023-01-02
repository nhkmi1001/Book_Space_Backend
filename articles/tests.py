from rest_framework.test import APITestCase
from django.urls import reverse
from articles.models import Book, Article, Comment
from users.models import User, Taste
from django.test import Client, TestCase

class ArticleViewCaseTest(TestCase):
    @classmethod
    def setUpTestData(self):
        Book.objects.create(book_title="흔한 남매 12", img_url="http://image.yes24.com/goods/1234/XL", book_content="어린시절", book_link="http://www.yes24.com/Product/Goods/74298443", book_genre="교육")
        Book.objects.create(book_title="ASDASD", img_url="http://image.yes24.com/goods/4324/XL", book_content="우연히", book_link="http://www.yes24.com/Product/Goods/74298444", book_genre="교육")
    
    def test_total_book(self):
        c = Client()
        response = c.get(reverse("article_view"))
        self.assertEqual(response.status_code, 200)
    
class PopularFeedViewCaseTest(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.user_data = {"email": "test@test.com", "username": "test", "password":"test1234"}
        self.user = User.objects.create(email="test@test.com", username="test", profile_img="fb-thankful", password="12341234",  )
        
        Article.objects.create(title="흔한 남매 12", content="asdasd", image="qwe.png", rating="4", created_at="2023-01-01 23:56:10", updated_at="2023-01-01 23:56:10", is_private="0", select_book_id="2", user=self.user)
        Article.objects.create(title="ASDASD", content="sdfsdfds", image="asd.png", rating="4", created_at="2023-01-01 23:56:10", updated_at="2023-01-01 23:56:10", is_private="0", select_book_id="2", user=self.user)

    def test_many_book(self):
        c = Client()
        response = c.get(reverse("popular_view"))
        self.assertEqual(response.status_code, 200)

class ManyBookViewCaseTest(APITestCase):
    @classmethod
    def setUpTestData(self):
        Book.objects.create(book_title="흔한 남매 12", img_url="http://image.yes24.com/goods/1234/XL", book_content="어린시절", book_link="http://www.yes24.com/Product/Goods/74298443", book_genre="교육")
        Book.objects.create(book_title="ASDASD", img_url="http://image.yes24.com/goods/4324/XL", book_content="우연히", book_link="http://www.yes24.com/Product/Goods/74298444", book_genre="교육")
    
    def test_total_book(self):
        c = Client()
        response = c.get(reverse("many_book_view"))
        self.assertEqual(response.status_code, 200)

class UserArticleViewCaseTest(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.user_data = {"email": "test@test.com", "username": "test", "password":"test1234"}
        self.user = User.objects.create_user("test@test.com", "test", "test1234")
        Taste.objects.create(user=self.user, choice=1)
        Taste.objects.create(user=self.user, choice=2)
        Taste.objects.create(user=self.user, choice=3)
        Book.objects.create(book_title="흔한 남매 12", img_url="http://image.yes24.com/goods/1234/XL", book_content="어린시절", book_link="http://www.yes24.com/Product/Goods/74298443", book_genre="교육")
        Book.objects.create(book_title="ASDASD", img_url="http://image.yes24.com/goods/4324/XL", book_content="우연히", book_link="http://www.yes24.com/Product/Goods/74298444", book_genre="교육")
    
    def setUp(self):
        self.access_token = self.client.post(reverse("user:token_obtain_pair_view"), self.user_data).data["access"]

    def test_user_machine_learning(self):
        response = self.client.get(
            path = reverse("user_article_view"),
            HTTP_AUTHORIZATION = f"Bearer {self.access_token}",
            data={"user_key":self.user.id}
        )
        self.assertEqual(response.status_code, 200)

class RecommendViewCaseTest(APITestCase):
    @classmethod
    def setUpTestData(self):
        Book.objects.create(book_title="흔한 남매 12", img_url="http://image.yes24.com/goods/1234/XL", book_content="어린시절", book_link="http://www.yes24.com/Product/Goods/74298443", book_genre="교육")
        Book.objects.create(book_title="ASDASD", img_url="http://image.yes24.com/goods/4324/XL", book_content="우연히", book_link="http://www.yes24.com/Product/Goods/74298444", book_genre="교육")
    def test_customlist_page_category(self):
        c = Client()
        response = c.get(
            path = reverse("recommend_view"),
            data={"genre_list": "교육"}
            )
        self.assertEqual(response.status_code, 200)
    
    def test_customlist_page_category_total(self):
        c = Client()
        response = c.get(
            path = reverse("recommend_view"),
            data={"genre_list": "전체"}
        )
        self.assertEqual(response.status_code, 200)

class ArticleListViewCaseTest(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.user_data = {"email": "test@test.com", "username": "test", "password":"test1234"}
        self.user = User.objects.create(email="test@test.com", username="test", profile_img="fb-thankful", password="12341234",  )
        
        Article.objects.create(title="흔한 남매 12", content="asdasd", image="qwe.png", rating="4", created_at="2023-01-01 23:56:10", updated_at="2023-01-01 23:56:10", is_private="0", select_book_id="2", user=self.user)
        Article.objects.create(title="ASDASD", content="sdfsdfds", image="asd.png", rating="3", created_at="2023-01-01 23:56:10", updated_at="2023-01-01 23:56:10", is_private="0", select_book_id="2", user=self.user)
    def test_time_sort(self):
        c = Client()
        response = c.get(
            path = reverse("main_list"),
            data={"rank":"시간순"}
        )
        self.assertEqual(response.status_code, 200)
    
    def test_like_sort(self):
        c = Client()
        response = c.get(
            path = reverse("main_list"),
            data={"rank":"좋아요순"}
        )
        self.assertEqual(response.status_code, 200)

    def test_comment_sort(self):
        c = Client()
        response = c.get(
            path = reverse("main_list"),
            data={"rank":"댓글순"}
        )
        self.assertEqual(response.status_code, 200)

class FeedChoiceBookViewCaseTest(APITestCase):
    @classmethod
    def setUpTestData(self):
        Book.objects.create(book_title="흔한 남매 12", img_url="http://image.yes24.com/goods/1234/XL", book_content="어린시절", book_link="http://www.yes24.com/Product/Goods/74298443", book_genre="교육")
        Book.objects.create(book_title="ASDASD", img_url="http://image.yes24.com/goods/4324/XL", book_content="우연히", book_link="http://www.yes24.com/Product/Goods/74298444", book_genre="교육")
        self.user_data = {"email": "test@test.com", "username": "test", "password":"test1234"}
        self.user = User.objects.create(email="test@test.com", username="test", profile_img="fb-thankful", password="12341234",  )
        
        Article.objects.create(title="흔한 남매 12", content="asdasd", image="qwe.png", rating="4", created_at="2023-01-01 23:56:10", updated_at="2023-01-01 23:56:10", is_private="0", select_book_id="2", user=self.user)
        Article.objects.create(title="ASDASD", content="sdfsdfds", image="asd.png", rating="3", created_at="2023-01-01 23:56:10", updated_at="2023-01-01 23:56:10", is_private="0", select_book_id="2", user=self.user)
    def test_feed_choice(self):
        book_id = 2
        c = Client()
        response = c.get(
            path = reverse("choice_book", kwargs={"book_id": book_id}),
        )
        self.assertEqual(response.status_code, 200)

class ArticleDetailViewCaseTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book1 = Book.objects.create(book_title="흔한 남매 12", img_url="http://image.yes24.com/goods/1234/XL", book_content="어린시절", book_link="http://www.yes24.com/Product/Goods/74298443", book_genre="교육")
        cls.book2 = Book.objects.create(book_title="ASDASD", img_url="http://image.yes24.com/goods/4324/XL", book_content="우연히", book_link="http://www.yes24.com/Product/Goods/74298444", book_genre="교육")
        cls.user_data = {"email": "test@test.com", "username": "test", "password":"test1234"}
        cls.user = User.objects.create_user("test@test.com", "test", "test1234", "profile_img")
        cls.comment_data = {"content":"123asd"}
        cls.article1 = Article.objects.create(title="흔한 남매 12", content="asdasd", image="qwe.png", rating="4", created_at="2023-01-01 23:56:10", updated_at="2023-01-01 23:56:10", is_private=False, select_book=cls.book1, user=cls.user)
        cls.article2 = Article.objects.create(title="ASDASD", content="sdfsdfds", image="asd.png", rating="3", created_at="2023-01-01 23:56:10", updated_at="2023-01-01 23:56:10", is_private=False, select_book=cls.book2, user=cls.user)

    def setUp(self):
        self.access_token = self.client.post(reverse("user:token_obtain_pair_view"), self.user_data).data["access"]

    def test_article_detail_get(self):
        article_id = 1
        c = Client()
        response = c.get(
            path = reverse("article_detail_view", kwargs={"article_id": article_id})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_article_detail_delete(self):
        article_id = 1
        response = self.client.delete(
            path = reverse("article_detail_view", kwargs={"article_id": article_id}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 204)

    def test_article_detail_comment_post(self):
        response = self.client.post(
            path = reverse("article_detail_view", kwargs={"article_id": 1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data = self.comment_data
        )
        self.assertEqual(response.status_code, 200)
    
    def test_article_detail_undefined_image_put(self):
        response = self.client.put(
            path = reverse("article_detail_view", kwargs={"article_id": 1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data={"image":"undefined", "title":"asd", "content":"asd"}
        )
        self.assertEqual(response.status_code, 200)
    
    def test_article_detail_defined_image_put(self):
        response = self.client.put(
            path = reverse("article_detail_view", kwargs={"article_id": 1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data={"content":"asd"}
        )
        self.assertEqual(response.status_code, 200)

class CreateArticleViewCaseTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book1 = Book.objects.create(book_title="흔한 남매 12", img_url="http://image.yes24.com/goods/1234/XL", book_content="어린시절", book_link="http://www.yes24.com/Product/Goods/74298443", book_genre="교육")
        cls.book2 = Book.objects.create(book_title="ASDASD", img_url="http://image.yes24.com/goods/4324/XL", book_content="우연히", book_link="http://www.yes24.com/Product/Goods/74298444", book_genre="교육")
        cls.user_data = {"email": "test@test.com", "username": "test", "password":"test1234"}
        cls.user = User.objects.create_user("test@test.com", "test", "test1234", "fb-thankful.png")
        cls.article_data = {"content":"adsasd", "rating":4, "image":"123465.png"}
        cls.article1 = Article.objects.create(title="흔한 남매 12", content="asdasd", image="qwe.png", rating=4, created_at="2023-01-01 23:56:10", updated_at="2023-01-01 23:56:10", is_private="0", select_book=cls.book1, user=cls.user)
        cls.article2 = Article.objects.create(title="ASDASD", content="sdfsdfds", image="asd.png", rating=3, created_at="2023-01-01 23:56:10", updated_at="2023-01-01 23:56:10", is_private="0", select_book=cls.book2, user=cls.user)

    def setUp(self):
        self.access_token = self.client.post(reverse("user:token_obtain_pair_view"), self.user_data).data["access"]

    def test_article_create_get(self):
        response = self.client.get(
            path = reverse("create_article_book", kwargs={"book_id":1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )        
        self.assertEqual(response.status_code, 200)

    def test_article_create_post(self):
        response = self.client.post(
            path = reverse("create_article_book", kwargs={"book_id":1}),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data = self.article_data
        )        
        self.assertEqual(response.status_code, 400)

class BookSearchViewCaseTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book1 = Book.objects.create(book_title="흔한 남매 12", img_url="http://image.yes24.com/goods/1234/XL", book_content="어린시절", book_link="http://www.yes24.com/Product/Goods/74298443", book_genre="교육")
        cls.book2 = Book.objects.create(book_title="ASDASD", img_url="http://image.yes24.com/goods/4324/XL", book_content="우연히", book_link="http://www.yes24.com/Product/Goods/74298444", book_genre="교육")
        cls.user_data = {"email": "test@test.com", "username": "test", "password":"test1234"}
        cls.user = User.objects.create_user("test@test.com", "test", "test1234")
        cls.article_data = {"title": "asd", "content":"adsasd", "rating":4, "image":"fb-thankful.png"}
        cls.article1 = Article.objects.create(title="흔한 남매 12", content="asdasd", image="qwe.png", rating="4", created_at="2023-01-01 23:56:10", updated_at="2023-01-01 23:56:10", is_private=False, select_book=cls.book1, user=cls.user)
        cls.article2 = Article.objects.create(title="ASDASD", content="sdfsdfds", image="asd.png", rating="3", created_at="2023-01-01 23:56:10", updated_at="2023-01-01 23:56:10", is_private=False, select_book=cls.book2, user=cls.user)
    
    def setUp(self):
        self.access_token = self.client.post(reverse("user:token_obtain_pair_view"), self.user_data).data["access"]

    def test_search_success(self):
        response = self.client.get(
            path=reverse("search_book"),
            data={"search_content": "흔한"},
        )
        self.assertEqual(response.status_code, 200)

    def test_search_book_post(self):
        response = self.client.post(
            path=reverse("search_book"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}", 
            data=self.article_data
        )
        self.assertEqual(response.status_code, 400)

class CommentEditViewCaseTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1_data = {"email":"test1@test.com", "username":"test1", "password":"test1234"}
        cls.user2_data = {"email":"test2@test.com", "username":"test2", "password":"test1234"}
        cls.user3_data = {"email":"test3@test.com", "username":"test3", "password":"test1234"}
        cls.comment_data = {"content": "test content"}
        cls.user1 = User.objects.create_user("test1@test.com", "test1", "test1234", "fb-thankful.png")
        cls.user2 = User.objects.create_user("test2@test.com", "test2", "test1234", "fb-thankful.png")
        cls.user3 = User.objects.create_user("test3@test.com", "test3", "test1234", "fb-thankful.png")
        cls.article1 = Article.objects.create(title="흔한 남매 12", content="asdasd", image="qwe.png", rating="4", created_at="2023-01-01 23:56:10", updated_at="2023-01-01 23:56:10", is_private="0", select_book_id="2", user=cls.user1)
        cls.article2 = Article.objects.create(title="ASDASD", content="sdfsdfds", image="asd.png", rating="3", created_at="2023-01-01 23:56:10", updated_at="2023-01-01 23:56:10", is_private="0", select_book_id="2", user=cls.user2)
        cls.article3 = Article.objects.create(title="sdfsdf", content="sdfsdfds", image="asd.png", rating="2", created_at="2023-01-01 23:56:10", updated_at="2023-01-01 23:56:10", is_private="0", select_book_id="2", user=cls.user3)

        cls.comment = Comment.objects.create(
            content="내용",
            user=cls.user1,
            article=cls.article1
        )
        cls.comment1 = Comment.objects.create(
            content="내용",
            user=cls.user2,
            article=cls.article2
        )
    def setUp(self):
        self.access_token_1 = self.client.post(reverse("user:token_obtain_pair_view"), self.user1_data).data["access"]
        self.access_token_2 = self.client.post(reverse("user:token_obtain_pair_view"), self.user2_data).data["access"]
        self.access_token_3 = self.client.post(reverse("user:token_obtain_pair_view"), self.user3_data).data["access"]
    
    def test_comment_edit_sucess(self):
        response = self.client.put(
            path=reverse("comment_edit_view", kwargs={"article_id":1, "comment_id":1}), 
            HTTP_AUTHORIZATION = f"Bearer {self.access_token_1}",
            data = {"content": "내용 수정"}
        )
        self.assertEqual(response.status_code, 200)
        
    #댓글 수정 실패(작성자 다름)
    def test_comment_edit_fail(self):
        response = self.client.put(
            path=reverse("comment_edit_view", kwargs={"article_id":1, "comment_id":1}), 
            HTTP_AUTHORIZATION = f"Bearer {self.access_token_2}",
            data = {"content": "내용 수정"}
        )
        self.assertEqual(response.status_code, 403)
    
    def test_comment_delete_success(self):
        response = self.client.delete(
            path=reverse("comment_edit_view", kwargs={"article_id":1, "comment_id":1}), 
            HTTP_AUTHORIZATION = f"Bearer {self.access_token_1}",
            data=self.comment_data
        )
        self.assertEqual(response.status_code, 204)
        
    def test_comment_delete_fail(self):
        response = self.client.delete(
            path=reverse("comment_edit_view", kwargs={"article_id":1, "comment_id":1}), 
            HTTP_AUTHORIZATION = f"Bearer {self.access_token_2}",
            data=self.comment_data
        )
        self.assertEqual(response.status_code, 403)

class LikeViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email":"test1@test.com", "username":"test1", "password":"test1234"}
        cls.comment_data = {"content": "test content"}
        cls.user = User.objects.create_user("test1@test.com", "test1", "test1234", "fb-thankful.png")
        cls.article = Article.objects.create(title="흔한 남매 12", content="asdasd", image="qwe.png", rating="4", created_at="2023-01-01 23:56:10", updated_at="2023-01-01 23:56:10", is_private="0", select_book_id="2", user=cls.user)
        Comment.objects.create(content="내용", user=cls.user, article=cls.article)

    def setUp(self):
        self.access_token = self.client.post(reverse("user:token_obtain_pair_view"), self.user_data).data["access"]
        
    def test_like_success(self):
        response = self.client.post(
            path=reverse("like_view", kwargs={"article_id":1}), 
            HTTP_AUTHORIZATION = f"Bearer {self.access_token}",
            data=self.comment_data
        )
        self.assertEqual(response.status_code, 200)
