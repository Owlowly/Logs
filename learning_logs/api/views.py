from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from learning_logs.models import Topic, Entry
from learning_logs.api.serializers import TopicSerializer, TopicsSerializer, ProfileSerializer
from account.models import Profile


class TopicListView(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicsSerializer
    pagination_class = PageNumberPagination


class TopicDetailView(generics.RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class UserFollowView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        profile = get_object_or_404(Profile, pk=pk)
        if request.user.pk == profile.user.pk:
            return Response({'error': 'You can not follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.user in profile.user_follow.all():
            return Response({'error': 'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)

        profile.user_follow.add(request.user)
        return Response({'success': True, 'message': 'Enrolled successfully'})


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class MyProfileViewSet(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile)

        # Include topics in the response
        topics = Topic.objects.filter(owner=request.user)
        topic_serializer = TopicSerializer(topics, many=True)

        data = {
            'profile': serializer.data,
            'topics': topic_serializer.data,
        }

        return Response(data)


class UserProfile(APIView):
    queryset= Profile.objects.all()

    def get(self, request, pk):
        profile = get_object_or_404(Profile, user__pk=pk)
        topics = Topic.objects.filter(owner=profile.user)

        topic_serializer = TopicSerializer(topics, many=True)
        profile_serializer = ProfileSerializer(profile)

        data = {
            'profile': profile_serializer.data,
            'topics': topic_serializer.data,
        }

        return Response(data)

class FollowedUsers(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()

    def get(self, request):
        user_profile = get_object_or_404(Profile, user=request.user)
        followed_profiles = user_profile.user_follow.all()
        serializer = ProfileSerializer(followed_profiles, many=True)
        data = {'followed_users': serializer.data}
        return Response(data)


class MostLikedTopics(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        """
        Get the most liked topics.
        """
        topics = Topic.objects.annotate(likes_count=Count('total_likes')).order_by('-likes_count')[:10]
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

