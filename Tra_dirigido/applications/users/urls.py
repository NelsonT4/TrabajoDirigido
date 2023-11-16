from django.urls import path
from . import views

app_name = 'users_app'

urlpatterns = [
    path('register/',
         views.UserRegisterView.as_view(),
         name='user-register'),
    path('index/',
         views.HomeUserView.as_view(),
         name='index'),
    path('loginUser/',
         views.LoginUser.as_view(),
         name='user-login'),
    path('logOut/',
         views.LogoutView.as_view(),
         name='user-logOut'),
    path('update/',
         views.UpdatePasswordView.as_view(),
         name='user-update'),
]
