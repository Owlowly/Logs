from django.urls import path, include
from rest_framework import routers
from . import views


topic_router = routers.DefaultRouter()
topic_router.register(r'', views.TopicViewSet, basename='topic')

app_name = 'api'

urlpatterns = [
    path('follow/<int:pk>/', views.UserFollowView.as_view(), name='user_follow'),
    path('most_liked_topics/', views.MostLikedTopics.as_view(), name='most_liked_topics'),
    path('my_profile/', views.MyProfileViewSet.as_view(), name='my_profile'),
    path('user_profile/<int:pk>/', views.UserProfile.as_view(), name='user_profile'),
    path('followed_profiles/', views.FollowedUsers.as_view(), name='followed_profiles'),
    path('', include(topic_router.urls)),

]
