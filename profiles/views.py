from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Profile, FollowRelation
from .serializers import (ProfileSerializer, FollowerRelationSerializer,
                          FollowingRelationSerializer)

User = get_user_model()


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_url_kwarg = 'profile_id'


class ProfileFollowView(APIView):
    def post(self, request, profile_id):
        profile = get_object_or_404(Profile, id=profile_id)
        user = request.user
        follow, created = FollowRelation.objects.get_or_create(user=user,
                                                               profile=profile)
        is_following = user in profile.followers.all()
        return Response({
            'is_following': is_following,
            'created': created
        },
                        status=status.HTTP_200_OK)


class FollowerRelationListView(generics.ListAPIView):
    queryset = FollowRelation.objects.all()
    serializer_class = FollowerRelationSerializer

    def get_queryset(self):
        profile_id = self.kwargs.get('profile_id')
        return FollowRelation.objects.filter(profile=profile_id)


class FollowerRelationDetailView(generics.RetrieveDestroyAPIView):
    queryset = FollowRelation.objects.all()
    serializer_class = FollowerRelationSerializer

    def get_object(self):
        profile_id = self.kwargs.get('profile_id')
        follow_id = self.kwargs.get('follow_id')
        return FollowRelation.objects.get(id=follow_id, profile=profile_id)


class FollowingRelationListView(generics.ListAPIView):
    queryset = FollowRelation.objects.all()
    serializer_class = FollowingRelationSerializer

    def get_queryset(self):
        profile_id = self.kwargs.get('profile_id')
        profile = Profile.objects.get(id=profile_id)
        user_id = profile.user.id
        return FollowRelation.objects.filter(user=user_id)


class FollowingRelationDetailView(generics.RetrieveDestroyAPIView):
    queryset = FollowRelation.objects.all()
    serializer_class = FollowingRelationSerializer

    def get_object(self):
        profile_id = self.kwargs.get('profile_id')
        profile = Profile.objects.get(id=profile_id)
        user_id = profile.user.id
        follow_id = self.kwargs.get('follow_id')
        return FollowRelation.objects.get(id=follow_id, user=user_id)
