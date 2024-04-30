from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = 'account'

urlpatterns = [

    path('register/', views.register, name='register'),
    path('profile_edit', views.edit, name='profile_edit'),
    path('profile/', views.profile, name='profile'),
    path('delete_user/<int:user_id>/', views.delete_user, name='confirm_delete_user'),
    path('all_users/', views.all_users, name='all_users'),
    path('follow/', views.user_follow, name='user_follow'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
    path('most_followed_users/', views.most_followed_users, name='most_followed_users'),
    path('followed_users/', views.followed_users, name='followed_users'),
    path('activity_feed/', views.activity_feed, name='activity_feed'),
    path('all_messages/', views.all_messages, name='all_messages'),
    path('user_messages/<str:username>/', views.user_messages, name='user_messages'),
    path('send_messages/<str:username>/', views.send_messages, name='send_messages'),
    path('confirm_delete_messages/<str:username>/', views.user_messages_delete, name='confirm_delete_messages'),
    path('confirm_delete_messages/<str:username>/', views.user_messages_delete, name='confirm_delete_messages'),
    path('', include('django.contrib.auth.urls')),

]