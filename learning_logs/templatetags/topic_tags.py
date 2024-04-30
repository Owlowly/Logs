from django import template
from ..models import Topic, Entry
from django.db.models import Count
from account.models import Profile

register = template.Library()

@register.simple_tag
def total_topics():
    return Topic.objects.count()

@register.inclusion_tag('learning_logs/latest_topics.html')
def show_latest_topics(count=5):
    latest_topics = Topic.objects.order_by('-date_added')[:count]
    return {'latest_topics': latest_topics}


@register.simple_tag
def get_most_commented_topics(count=5):
    return Topic.objects.annotate(total_comments=Count('entries')).order_by('-total_comments')[:count]


@register.simple_tag
def get_most_liked_topics():
    # most_liked_topics = Topic.objects.annotate(like_count=Count('users_like')).order_by('-like_count')[:5]
    most_liked_topics = Topic.objects.order_by('-total_likes')[:5]
    return most_liked_topics


@register.filter(name='user_topic_count')
def user_topic_count(user):
    return Topic.objects.filter(owner=user).count()