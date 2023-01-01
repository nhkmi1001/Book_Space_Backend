from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Q
from articles.models import Article, Comment, Book
from users.models import User, Taste
from articles.serializers import ArticleSerializer, ArticleCreateSerializer, ArticleDetailSerializer, CommentCreateSerializer, BookSerializer,BookRecommendSerializer, ArticleAddSerializer, ArticlePutSerializer, ArticleUserSerializer, ManyBookListSerializer
from rest_framework.generics import get_object_or_404
from django.db.models import Count
import json
from articles import crowling
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from articles.recom import recommendation
from drf_yasg.utils import swagger_auto_schema


# 파일 저장
import random
import json , csv, os, requests

import django
from django.db.models import Count

from django.db.models import Count

django.setup()

A = Book.objects.aggregate(Count('id'))
B = str(A).split(':')[1].split('}')[0].split(' ')[1]
print(B)

if int(B) < 320:
   crowling.function()
else:
    pass


class ArticleView(APIView): #메인페이지 전체리스트
    def get(self, request):
        best_list = Book.objects.all()
        serializer = BookSerializer(best_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PopularFeedView(APIView): # 메인페이지 인기피드
    def get(self, request):
        popular_articles_list = Article.objects.annotate(num_likes=Count('likes')).order_by('-num_likes', 'id')[:3]
        serializer = ArticleSerializer(popular_articles_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManyBookView(APIView): #많이 선택 된 책
    def get(self, request):
        a = Book.objects.all().annotate(num_likes=Count('article')).order_by('-num_likes', 'id')[:3]
        serializer = ManyBookListSerializer(a, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserArticleView(APIView): #추천머신러닝을 통한 결과물 메인페이지에 보여줄거
    def get(self, request):
        user_key = request.GET['user_key']
        book_id_list = []
        taste_id = Taste.objects.filter(user_id=int(user_key))
        for i in taste_id:
            book_id_list.append(i.choice)
        recom_result = []
        for j in book_id_list:
            recommend_list = recommendation(j)
            try:
                for a in recommend_list:
                    recom_result.append(a)
            except TypeError:
                pass
        result_list = []
        for result in recom_result:
            result_book = Book.objects.get(id=result)
            result_list.append(result_book)
        serializer = BookSerializer(result_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RecommendView(APIView):
    def get(self, request):
        genre = request.GET.get("genre_list", None)

        if genre == "전체":
            show_book = Book.objects.all()
        else:
            Test = request.GET["genre_list"]
            show_book = Book.objects.filter(book_genre = Test)
        show_book_list = random.sample(list(show_book),10)
        serializer = BookSerializer(show_book_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ArticleListView(APIView): # 피드페이지
    def get(self, request):
        rank = request.GET.get("rank", None)
        if rank == "시간순":
            articles_list = Article.objects.filter(is_private=False).order_by("-created_at")
        elif rank == "좋아요순":
            articles_list = Article.objects.filter(is_private=False).annotate(num_likes=Count('likes')).order_by('-num_likes', '-rating')
        elif rank == "댓글순":
            articles_list = Article.objects.filter(is_private = False).annotate(num_comments=Count('comment')).order_by('-num_comments', '-rating')
        else:
            articles_list = Article.objects.filter(is_private=False).order_by("-rating")
        serializer = ArticleSerializer(articles_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FeedChoiceBookView(APIView):
    def get(self, request, book_id):
        articles = Article.objects.filter(select_book =book_id).annotate(num_likes=Count('likes')).order_by('-num_likes')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ArticleDetailView(APIView):
    def get(self, request, article_id): # 게시글&댓글 보여주기
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary="게시글 삭제",
        responses={200:"성공", 401:"인증 오류", 403:"접근 권한 에러", 500:"서버 에러"},
    )
    def delete(self, request, article_id): # 게시글 삭제하기
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("작성자가 아닙니다!", status=status.HTTP_403_FORBIDDEN)
        
    @swagger_auto_schema(
        request_body=CommentCreateSerializer,
        operation_summary="댓글 작성",
        responses={200:"성공", 400:"잘못된 요청", 401:"권한 없음", 500:"서버 에러"}
    )
    def post(self, request, article_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
        request_body=ArticlePutSerializer,
        operation_summary="게시글 수정",
        responses={200:"성공", 400:"잘못된 요청", 401:"권한 없음", 500:"서버 에러"}
    )
    def put(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        data=request.data
        image=data.get("image")
        if request.user == article.user:
            if image == "undefined":
                data = dict({key: value for key, value in data.items() if value != "undefined"})
                serializer = ArticlePutSerializer(article, data = data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = ArticlePutSerializer(article, data = data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("작성자가 아닙니다!", status=status.HTTP_403_FORBIDDEN)

class CreateArticleView(APIView):
    def get(self, request, book_id):
        book_id = get_object_or_404(Book, id=book_id)
        serializer = BookRecommendSerializer(book_id)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=ArticleAddSerializer,
        operation_summary="게시글 작성 책 있을 때",
        responses={200:"성공", 400:"잘못된 요청", 401:"권한 없음", 500:"서버 에러"}
    )
    def post(self, request, book_id): #피드페이지에서 검색해서 책 선택하고 게시글 작성으로 갈 때 post
        book = get_object_or_404(Book, id=book_id)
        title = book.book_title
        book_id = book.id
        serializer = ArticleAddSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, select_book_id=book_id, title=title)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookSearchView(APIView): #무슨책 있는지 검색하는 곳
    def get(self, request):
        search_title = request.GET.get('search_content')
        if search_title == None :
            book = Book.objects.all()
        elif search_title:
            search_title = search_title.replace(" ","")
            book = Book.objects.filter(Q(book_title__icontains=search_title))
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=ArticleCreateSerializer,
        operation_summary="게시글 작성 책 없을 때",
        responses={200:"성공", 400:"잘못된 요청", 401:"권한 없음", 500:"서버 에러"}
    )
    def post(self, request): # 새로작성 하기 버튼 눌렀을 때
        serializer = ArticleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) # True면 여기서 코드가 끝남
        serializer.save(user=request.user)
        return Response(serializer.data)



class CommentEditView(APIView):
    @swagger_auto_schema(
        request_body=CommentCreateSerializer,
        operation_summary="댓글 수정",
        responses={200:"성공", 400:"잘못된 요청", 401:"권한 없음", 500:"서버 에러"}
    )
    def put(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("작성자가 아닙니다!", status=status.HTTP_403_FORBIDDEN)
        
    @swagger_auto_schema(
        operation_summary="댓글 삭제",
        responses={200:"성공", 400:"잘못된 요청", 401:"권한 없음", 500:"서버 에러"}
    )    
    def delete(self, request, comment_id, article_id):
        comment = get_object_or_404(Comment, id=comment_id)
        article = get_object_or_404(Article, id=article_id)
        if request.user == comment.user or request.user == article.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("작성자가 아닙니다!", status=status.HTTP_403_FORBIDDEN)


class LikeView(APIView): #좋아요
    @swagger_auto_schema(
        operation_summary="좋아요",
        responses={200:"성공", 400:"잘못된 요청", 401:"권한 없음", 500:"서버 에러"}
    )
    def post(self, request, article_id):
        article = get_object_or_404(Article, id = article_id)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response({"message":"좋아요 취소 완료!"}, status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response({"message":"좋아요 등록 완료!"}, status=status.HTTP_200_OK)


class BookListPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookListView(APIView): #페이지네이션
        serializer_class = BookSerializer
        pagination_class = BookListPagination
        @property
        def paginator(self):
            if not hasattr(self, '_paginator'):
                if self.pagination_class is None:
                    self._paginator = None
                else:
                    self._paginator = self.pagination_class()
            else:
                pass
            return self._paginator
        def paginate_queryset(self, queryset):
            if self.paginator is None:
                return None
            return self.paginator.paginate_queryset(queryset, self.request, view=self)
        def get_paginated_response(self, data):
            assert self.paginator is not None
            return self.paginator.get_paginated_response(data)
        def get(self, request, format=None):
            book_list = Book.objects.all()
            page = self.paginate_queryset(book_list)
            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
            else:
                serializer = self.serializer_class(book_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)






# csv 만들기
# with open('bookdata.csv', 'w', newline='') as csvfile:
#     fieldnames = ['book_id','book_title','book_genre']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     writer.writeheader()

#     for book in Book.objects.all():
#         writer.writerow({'book_id':book.id, "book_title":book.book_title, "book_genre":book.book_genre})


