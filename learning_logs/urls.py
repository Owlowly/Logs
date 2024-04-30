from django.urls import path
from . import views
from django.conf.urls.static import static


app_name = 'learning_logs'

urlpatterns = [
    path('all_topics/', views.all_topics, name='all_topics'),
    # Page show all topics
    path('topics/', views.topics, name='topics'),
    path('tag/<slug:tag_slug>/', views.all_topics, name='topic_list_by_tag'),
    # Detail page for a single topic
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Adding new topic
    path('new_topic/', views.new_topic, name='new_topic'),
    # adding new entry
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # editing an entry
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    # editing the topic
    path('edit_topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    # delete topic
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='confirm_delete_topic'),
    # delete comment
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='confirm_delete_entry'),
    # share
    path('<int:topic_id>/share/', views.share_post, name='share_post'),
    # search
    path('search/', views.topic_search, name='topic_search'),
    # topic like
    path('like/', views.topic_like, name='like'),
    # most liked topics
    path('most_liked_topics/', views.most_liked_topics, name='most_liked_topics'),
    # ranking topics
    path('most_viewed/', views.most_viewed, name='most_viewed'),
    # liked topics
    path('liked_topics/', views.liked_topics, name='liked_topics'),
    # api page
    path('api_page/', views.api_page, name='api_page'),
    # privacy policy
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    # contact
    path('contact/', views.contact_view, name='contact'),
    path('contact/success/', views.success_view, name='contact_success'),


    # Home page
    path('', views.index, name='index'),

]