from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from api.views import \
    RegisterApiView, \
    PostApiView, \
    PostListApiView, \
    LikeView, UnlikeView, \
    PostLikesAnalyticsView, UserActivityView

urlpatterns = [
    path('login/', obtain_jwt_token, name='jwt_login'),
    path('register/', RegisterApiView.as_view()),
    path('create/', PostApiView.as_view()),
    path('posts/', PostListApiView.as_view()),
    path('posts/<int:pk>/like/', LikeView.as_view()),
    path('posts/<int:pk>/unlike/', UnlikeView.as_view()),
    path('analitics/date_from=<date_from>&date_to=<date_to>/', PostLikesAnalyticsView.as_view()),
    path('user_activity/', UserActivityView.as_view()),
]
