from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("<int:post_id>", views.post_view, name="post_view"),
    path("post-create/", views.post_create, name="post_create"),
    path("<post_id>/update", views.post_update, name="post_update"),
    path("<post_id>/delete", views.post_delete, name="post_delete"),
    path('post/like/<post_id>/', views.toggle_like, name='toggle_like'),
    path('feed/', views.news_feed, name='news_feed'),
]

