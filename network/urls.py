
from django.urls import path

from . import views

app_name = "network"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("following", views.following, name="following"),
    path("profile", views.profile, name="profile"),
    path("edit", views.edit, name="edit"),
    path("fetch_data", views.fetch_data, name="fetch_data"),
    path("post_data", views.post_data, name="post_data"),    
    path("user_profile/<str:username>/", views.user_profile, name="user_profile"),
    path("error", views.error, name="error"), 
]
