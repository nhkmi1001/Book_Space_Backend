from django.urls import path
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView, )
from users import views

app_name = 'user'
urlpatterns = [
    path('signup/', views.UserView.as_view(), name="user_view"),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair_view'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('<int:user_id>/', views.MypageView.as_view(), name='mypage_view'),
    path('<int:user_id>/likes/', views.LikeArticlesView.as_view(), name="like_articles_view"), #좋아요 게시글 보기
    path('<int:user_id>/image/', views.MypageImage.as_view(), name='mypage_image_view'),
    path('most-numberous/', views.MostNumberousBook.as_view(), name='most_numberous_view'),
    path('user-choice/', views.UserChoiceBook.as_view(), name='user_choice_book_view'),
    path('', views.RecommendView.as_view(), name='recommend_view'),
    path('activate/<str:uidb64>/<str:token>/', views.UserActivate.as_view(), name='activate'),
    
]
