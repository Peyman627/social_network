from rest_framework import generics

from .models import Post, PostLike
from .serializers import PostSerializer, PostLikeSerializer


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = 'post_id'


class PostLikeCreateView(generics.CreateAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer


class PostLikeListView(generics.ListAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return PostLike.objects.filter(post=post_id)


class PostLikeDetailView(generics.RetrieveDestroyAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

    def get_object(self):
        post_id = self.kwargs.get('post_id')
        like_id = self.kwargs.get('like_id')
        return PostLike.objects.get(id=like_id, post=post_id)
