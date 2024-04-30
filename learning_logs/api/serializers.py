from rest_framework import serializers
from learning_logs.models import Topic, Entry
from taggit.serializers import TaggitSerializer, TagListSerializerField
from account.models import Profile


class TopicsSerializer(TaggitSerializer, serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    owner = serializers.StringRelatedField()

    class Meta:
        model = Topic
        fields = ['id', 'url', 'text', 'tags', 'owner']

    def get_url(self, obj):
        return obj.get_absolute_url()


class EntrySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Entry
        fields = ['user', 'text', 'date_added']


class TopicSerializer(TaggitSerializer, serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    owner = serializers.StringRelatedField()
    entries = EntrySerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'url', 'text',  'body', 'date_added', 'owner', 'tags', 'total_likes', 'total_views', 'entries']

    def get_url(self, obj):
        return obj.get_absolute_url()


class ProfileSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    username = serializers.StringRelatedField()

    class Meta:
        model = Profile
        fields = ['id','username', 'created', 'total_followers', 'topics']