from rest_framework import serializers
from articles.models import Article, Comment, Book


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Comment
        fields = ("user", "content", "created_at", "updated_at", "id")


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)


class ArticleDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many=True)
    created_at = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    def get_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Article
        fields = "__all__"



class ArticleSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    def get_likes_count(self, obj):


        return obj.likes.count()

    def get_username(self, obj):
        return obj.user.username

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Article
        fields = "__all__"


class ArticleCreateSerializer(serializers.ModelSerializer): # 게시글 작성 시리얼라이즈
    class Meta:
        model = Article
        fields = ("title", "image", "content","select_book", "rating")

class ArticleImageSerializer(serializers.ModelSerializer):# 마이페이지에 모든 게시글이미지를 들고오기 위한 시리얼라이즈
    class Meta:
        model = Article
        fields = ("image","id")



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class BookRecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id",)