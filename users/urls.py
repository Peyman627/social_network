from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('email-verify/', views.EmailVerifyView.as_view(),
         name='email_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
