from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create-like/',
         views.PostLikeCreateView.as_view(),
         name='post_like_create'),
    path('<int:post_id>/likes/',
         views.PostLikeListView.as_view(),
         name='post_like_list'),
    path('<int:post_id>/likes/<int:like_id>/',
         views.PostLikeDetailView.as_view(),
         name='post_like_detail'),
]
