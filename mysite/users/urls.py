from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('profile/<username>', views.profile, name='profile'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('follow-unfollow/<username>/', views.follow_unfollow, name='follow_unfollow'),
    # path('unfollow/<username>/', views.unfollow_user, name='unfollow_user'),
    path('followers/<username>/', views.followers_list, name='followers_list'),
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]