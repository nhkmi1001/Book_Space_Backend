from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from articles.models import Article
from .models import User, Taste
from users.serializers import UserSerializer, UserMypageSerializer, RecommendSerializer, UserImageSerializer, MainNumberousBookSerializer, UserChoiceBookSerializer, UserNameSerializer,UserPasswordSerializer
from articles.serializers import ArticleImageSerializer
from articles.models import Article
from django.db.models import Q
from django.db.models import Count
from django.shortcuts import redirect

from rest_framework_simplejwt.views import ( TokenObtainPairView,TokenRefreshView, )
from users.serializers import CustomTokenObtainPairSerializer
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from users.token import account_activation_token
import traceback
from drf_yasg.utils import swagger_auto_schema
class UserView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        operation_summary = "회원가입",
        responses={201:"성공", 400:"잘못된 요청", 404:"찾을 수 없음", 500:"서버 에러"}
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserActivate(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        try:
            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                return redirect("http://127.0.0.1:5500/templates/email-done.html")
            else:
                return Response('만료된 링크입니다.', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(traceback.format_exc())

        
    
            
class MypageView(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        serializer = UserMypageSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        request_body=UserNameSerializer,
        operation_summary="회원정보 수정",
        responses={200:"성공", 400:"잘못된 요청", 401:"인증 오류", 404:"찾을 수 없음", 500:"서버 에러"}
    )
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        data = request.data
        if request.user == user:
            if data['password'] =="":
                data = dict({key:value for key, value in data.items() if value !=""})
                serializer = UserNameSerializer(user, data = request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif data['username'] =="":
                data = dict({key:value for key, value in data.items() if value !=""})
                serializer = UserPasswordSerializer(user, data = request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = UserSerializer(user, data = request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.!", status=status.HTTP_403_FORBIDDEN)
    @swagger_auto_schema(
        operation_summary="회원 탈퇴",
        responses={200:"성공", 401:"인증 오류", 403:"접근 권한 에러", 500:"서버 에러"}
    )
    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user == request.user:
            user.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response("해당 사용자가 아닙니다.", status=status.HTTP_401_UNAUTHORIZED)

class LikeArticlesView(APIView):
    def get(self, request, user_id):
        book = Article.objects.filter(Q(likes=user_id))
        serializer = ArticleImageSerializer(book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MypageImage(APIView): #프로필 이미지만 수정파트
    @swagger_auto_schema(
        request_body=UserImageSerializer,
        operation_summary="유저 프로필 이미지 수정",
        responses={200:"성공", 400:"잘못된 요청", 401:"인증 오류", 404:"찾을 수 없음", 500:"서버 에러"}
    )
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = UserImageSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.!", status=status.HTTP_403_FORBIDDEN)


class RecommendView(APIView):
    def post(self, request):
        serializer = RecommendSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class MostNumberousBook(APIView):
    def get(self, request):
        user = User.objects.all().annotate(num_likes=Count('article')).order_by('-num_likes', 'id')[:3]
        serializer = MainNumberousBookSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChoiceBook(APIView):
    @swagger_auto_schema(
        request_body=UserChoiceBookSerializer,
        operation_summary="사용자가 선택한 책 리스트",
        responses={200:"성공", 400:"잘못된 요청", 500:"서버 에러"}
    )
    def post(self, request):
        book_dict = request.data
        book_list = book_dict.get("choice")
        user = Taste.objects.filter(user_id=request.user)
        if user.count() >= 1:
            user.delete()
        for i in book_list:
            serializer = UserChoiceBookSerializer(data={"choice":i})
            if serializer.is_valid():
                serializer.save(user=request.user)
        return Response(serializer.data)



