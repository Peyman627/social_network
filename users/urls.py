from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'users'
urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('email-verify/', views.EmailVerifyView.as_view(),
         name='email_verify'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('password-reset/',
         views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/<uidb64>/<token>/',
         views.PasswordTokenCheckView.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         views.SetNewPasswordView.as_view(),
         name='password_reset_complete'),
]
