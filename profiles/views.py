from rest_framework import generics
from django.contrib.auth import get_user_model

from .models import Profile
from .serializers import ProfileSerializer, UserSerializer

User = get_user_model()


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_url_kwarg = 'profile_id'
