from rest_framework import generics
from django.contrib.auth import get_user_model

from .models import Profile, FollowerRelation
from .serializers import ProfileSerializer, FollowerRelationSerializer

User = get_user_model()


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_url_kwarg = 'profile_id'


class FollowerRelationListView(generics.ListCreateAPIView):
    queryset = FollowerRelation.objects.all()
    serializer_class = FollowerRelationSerializer

    def get_queryset(self):
        profile_id = self.kwargs.get('profile_id')
        return FollowerRelation.objects.filter(profile=profile_id)


class FollowerRelationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FollowerRelation.objects.all()
    serializer_class = FollowerRelationSerializer

    def get_object(self):
        profile_id = self.kwargs.get('profile_id')
        follow_id = self.kwargs.get('follow_id')
        return FollowerRelation.objects.get(id=follow_id, profile=profile_id)
