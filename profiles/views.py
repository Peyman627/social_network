from rest_framework import generics
from django.contrib.auth import get_user_model

from .models import Profile, FollowRelation
from .serializers import (ProfileSerializer, FollowerRelationSerializer,
                          FollowingRelationSerializer)

User = get_user_model()


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_url_kwarg = 'profile_id'


class FollowerRelationListView(generics.ListCreateAPIView):
    queryset = FollowRelation.objects.all()
    serializer_class = FollowerRelationSerializer

    def get_queryset(self):
        profile_id = self.kwargs.get('profile_id')
        return FollowRelation.objects.filter(profile=profile_id)


class FollowerRelationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FollowRelation.objects.all()
    serializer_class = FollowerRelationSerializer

    def get_object(self):
        profile_id = self.kwargs.get('profile_id')
        follow_id = self.kwargs.get('follow_id')
        return FollowRelation.objects.get(id=follow_id, profile=profile_id)


class FollowingRelationListView(generics.ListCreateAPIView):
    queryset = FollowRelation.objects.all()
    serializer_class = FollowingRelationSerializer

    def get_queryset(self):
        profile_id = self.kwargs.get('profile_id')
        profile = Profile.objects.get(id=profile_id)
        user_id = profile.user.id
        return FollowRelation.objects.filter(user=user_id)


class FollowingRelationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FollowRelation.objects.all()
    serializer_class = FollowingRelationSerializer

    def get_object(self):
        profile_id = self.kwargs.get('profile_id')
        profile = Profile.objects.get(id=profile_id)
        user_id = profile.user.id
        follow_id = self.kwargs.get('follow_id')
        return FollowRelation.objects.get(id=follow_id, user=user_id)
