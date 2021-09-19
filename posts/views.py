from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import Post, PostLike
from .serializers import PostSerializer, PostLikeSerializer
from profiles.permissions import IsOwnerOrReadOnly


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_url_kwarg = 'post_id'


class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        like, created = PostLike.objects.get_or_create(user=user, post=post)
        is_liked = user in post.likes.all()
        return Response({
            'is_liked': is_liked,
            'created': created
        },
                        status=status.HTTP_200_OK)


class PostLikeListView(generics.ListAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return PostLike.objects.filter(post=post_id)


class PostLikeDetailView(generics.RetrieveDestroyAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        post_id = self.kwargs.get('post_id')
        like_id = self.kwargs.get('like_id')
        return PostLike.objects.get(id=like_id, post=post_id)
