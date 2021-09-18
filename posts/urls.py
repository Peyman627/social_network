from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
]
