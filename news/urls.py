from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.user_login, name="login"),
    path("signup/", views.user_signup, name="signup"),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('submit_post/', views.submit_post, name='submit_post'),
    path("post/<int:post_id>", views.post, name="post"),
    path("user-comments/<str:username>/", views.user_comments, name="user_comments"),
    path("post/<int:post_id>/comments/", views.post_comments, name="post_comments"),

]