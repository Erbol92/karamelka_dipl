
from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from . import views


urlpatterns = [
    path('', views.auth, name='auth'),
    path('exit', views.exit, name='exit'),
    path('registration', views.registration, name='registration'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
    path('profile', views.profile, name='profile'),
    path('password-reset/',
         PasswordResetView.as_view(template_name="user_manager/templates/password_reset_form.html"),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name="user_manager/templates/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="user_manager/templates/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="user_manager/templates/password_reset_complete.html"), name='password_reset_complete'),
]

