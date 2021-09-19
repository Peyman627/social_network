from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('discover/',
         cache_page(60 * 10)(views.PostListDiscoverView.as_view()),
         name='post_list_discover'),
    path('feed/', (views.PostFeedView.as_view()), name='post_feed'),
    path('<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/like/', views.PostLikeView.as_view(),
         name='post_like'),
    path('<int:post_id>/likes/',
         views.PostLikeListView.as_view(),
         name='post_like_list'),
    path('<int:post_id>/likes/<int:like_id>/',
         views.PostLikeDetailView.as_view(),
         name='post_like_detail'),
]
