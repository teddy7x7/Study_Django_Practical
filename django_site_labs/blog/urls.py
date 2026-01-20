from django.urls import path
from . import views

app_name = "blog" # Namespace for the name field of the path, eg. {% url 'blog:posts_list' %}

urlpatterns = [
    path("", views.index, name="index"),
    path("posts", views.posts_list, name="posts_list"),
    path("posts/<slug:slug>", views.post_detail, name="post_detail"), # /post/first-post
]
