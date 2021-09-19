from django.urls import path

from . import views

app_name = 'profiles'
urlpatterns = [
    path('', views.ProfileListView.as_view(), name='profile_list'),
    path('<int:profile_id>/',
         views.ProfileDetailView.as_view(),
         name='profile_detail'),
    path('<int:profile_id>/follow/',
         views.ProfileFollowView.as_view(),
         name='profile_follow'),
    path('<int:profile_id>/followers/',
         views.FollowerRelationListView.as_view(),
         name='follower_relation_list'),
    path('<int:profile_id>/followers/<int:follow_id>/',
         views.FollowerRelationDetailView.as_view(),
         name='follower_relation_detail'),
    path('<int:profile_id>/followings/',
         views.FollowingRelationListView.as_view(),
         name='following_relation_list'),
    path('<int:profile_id>/followings/<int:follow_id>/',
         views.FollowingRelationDetailView.as_view(),
         name='following_relation_detail'),
]
