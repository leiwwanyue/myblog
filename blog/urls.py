from captcha.views import captcha_refresh
from django.urls import path, include
from django.views.generic import TemplateView

from . import views
from .views import LoginView, PasswordResetRequestView, PasswordResetConfirmView
from .views import request_verification_code, login_with_verification_code


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post_list', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('profile/<int:pk>', views.user_profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('post/', views.post_list, name='post_list'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password_reset/done/', TemplateView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', TemplateView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('captcha/', include('captcha.urls')),
    path('refresh/', captcha_refresh),
    path('api/request_verification_code/', request_verification_code, name='request_verification_code'),
    path('api/login_with_verification_code/', login_with_verification_code, name='login_with_verification_code'),

]
