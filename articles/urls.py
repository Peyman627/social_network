from django.urls import path

from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('<int:article_id>/',
         views.ArticleDetailView.as_view(),
         name='article_detail'),
]
