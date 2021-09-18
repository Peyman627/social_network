from django.urls import path

from . import views

app_name = 'profiles'
urlpatterns = [
    path('<int:profile_id>/',
         views.ProfileDetailView.as_view(),
         name='profile_detail'),
    path('<int:profile_id>/follows/',
         views.FollowerRelationListView.as_view(),
         name='follower_relation_list'),
    path('<int:profile_id>/follows/<int:follow_id>/',
         views.FollowerRelationDetailView.as_view(),
         name='follower_relation_detail'),
]
