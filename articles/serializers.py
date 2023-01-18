from rest_framework import serializers
from articles.models import Article, Comment, Book
from users.models import User
from django.urls import path
# from users.serializers import UserMypageSerializer



class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    profile_img = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_user_id(self, obj):
        return obj.user.id

    def get_profile_img(self, obj):
        return obj.user.profile_img.url
    
    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Comment
        fields = ("user", "content", "created_at", "updated_at", "id", "profile_img", "user_id")


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)


class ArticleDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many=True)
    updated_at = serializers.SerializerMethodField()
    profile_img = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_user_id(self, obj):
        return obj.user.id

    def get_updated_at(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_profile_img(self, obj):
        return obj.user.profile_img.url

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    class Meta:
        model = Article
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class ArticleSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    profile_img = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many=True)

    class Meta:
        model = Article
        fields = "__all__"

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_username(self, obj):
        return obj.user.username

    def get_profile_img(self, obj):
        return obj.user.profile_img.url

    def get_user_id(self, obj):
        return obj.user.id


class ArticleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"

class ArticleAddSerializer(serializers.ModelSerializer): #책을 선택 후 게시글 작성
    class Meta:
        model = Article
        fields = ("image", "content", "rating", "is_private")


class ArticleCreateSerializer(serializers.ModelSerializer): # 게시글 작성 시리얼라이즈
    class Meta:
        model = Article
        fields = ("title", "image", "content", "rating", "is_private")

    def create(self, validated_data):
        Book.objects.create(book_title=validated_data.get('title', ''))

        return super().create(validated_data) # super가 부모 class에 존재하는 create함수를 실행시켜준다.


class ArticlePutSerializer(serializers.ModelSerializer): # 게시글 작성 시리얼라이즈
    class Meta:
        model = Article
        fields = ("content", "image", "is_private")


class ArticleImageSerializer(serializers.ModelSerializer):# 마이페이지에 모든 게시글이미지를 들고오기 위한 시리얼라이즈
    class Meta:
        model = Article
        fields = ("image","id", "likes")


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class BookRecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id","book_title")


class ManyBookListSerializer(serializers.ModelSerializer):
    article_count = serializers.IntegerField(source='article_set.count', read_only=True)
    class Meta:
        model = Book
        fields = ("book_title", "article_count")

