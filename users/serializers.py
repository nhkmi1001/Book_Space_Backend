from rest_framework import serializers
from users.models import User, Taste
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from articles.serializers import ArticleImageSerializer, BookRecommendSerializer
from users.token import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import check_password
import threading

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
        
    def run(self):
        self.email.send()

class UserSerializer(serializers.ModelSerializer):
    passwordcheck = serializers.CharField(style={'input_type':'password'}, required=False)

    class Meta:
        model = User
        fields = ('email','username' ,'password','passwordcheck')
        extra_kwargs={
            'password':{'write_only':True, 'required': False},

        }        
        
    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.is_active = False
        user.save()
        message = render_to_string('user/account_activate_email.html', {
          'user': user,
          'domain': 'localhost:8000',
          'uid': urlsafe_base64_encode(force_bytes(user.pk)),
          'token': account_activation_token.make_token(user),
        })
        mail_subject = 'Thumbook 회원가입 인증 이메일입니다.'
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        EmailThread(email).start()
        email.content_subtype = "html"
        return validated_data
    

    def update(self, obj, validated_data):
        obj.username = validated_data.get('username', obj.username)
        obj.password = validated_data.get('password', obj.password)
        obj.set_password(obj.password)
        obj.save()
        return obj

    def validate(self, data):
        password=data.get('password')
        passwordcheck=data.pop('passwordcheck')
        print(passwordcheck)

        if password != passwordcheck:
            raise serializers.ValidationError(
                detail={"error":"비밀번호가 맞지 않습니다"}
            )

        if not len(data.get("password", "")) >= 8:
            raise serializers.ValidationError(
                detail={"error": "password의 길이는 8자리 이상이어야합니다."}
            )

        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError(
                detail=("password는 영문 숫자 조합으로 구성되어야 합니다.")
            )

        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError("이메일이 이미 존재합니다.")
        return data

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)

class UserPasswordSerializer(serializers.ModelSerializer):
    passwordcheck = serializers.CharField(style={'input_type':'password'}, required=False)
    class Meta:
        model = User
        fields = ("password", "passwordcheck")
    def update(self, obj, validated_data):
        obj.password = validated_data.get('password', obj.password)
        obj.set_password(obj.password)
        obj.save()
        return obj


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['userpk'] = user.pk
        return token


    def validate(self,data):
        if not User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("이메일이 존재하지 않습니다.")

        if User.objects.get(email=data['email']).is_active == False:
            raise serializers.ValidationError("이메일 인증이 필요합니다.")

        if (check_password(data['password'],User.objects.get(email=data['email']).password)) == False:
            raise serializers.ValidationError("비밀번호가 틀렸습니다.")

        result =super().validate(data)

        refresh = self.get_token(self.user)

         # response에 추가하고 싶은 key값들 추가
        result['username'] = self.user.username
        result['refresh'] = str(refresh)
        result['access'] = str(refresh.access_token)
        result['email'] = self.user.email
        result['userpk'] = self.user.pk
        result['is_active'] = self.user.is_active
        result['password'] = self.user.password
        result['success'] = True

        return result


class UserMypageSerializer(serializers.ModelSerializer): #마이페이지를 위한 시리얼라이즈
    article_set = ArticleImageSerializer(many=True)
    class Meta:
        model = User
        fields =  ("id","username", "article_set", "profile_img", )

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("profile_img",)


class RecommendSerializer(serializers.ModelSerializer):
    select_books = BookRecommendSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ("select_books",)


class MainNumberousBookSerializer(serializers.ModelSerializer):
    article_count = serializers.IntegerField(source='article_set.count', read_only=True)
    class Meta:
        model = User
        fields =  ("id","username", "article_count")



class UserChoiceBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taste
        fields = ("choice",)

