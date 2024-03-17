from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.user_login, name="login"),
    path("signup/", views.user_signup, name="signup"),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<str:username>/', views.general_profile, name='general_profile'),
    path('submit_post/', views.submit_post, name='submit_post'),
    path("user-comments/<str:username>/", views.user_comments, name="user_comments"),
    path("user-posts/<str:username>/", views.user_posts, name="user_posts"),
    path("post/<int:post_id>/comments/", views.post_comments, name="post_comments"),
    path('comment/<int:comment_id>/submit_reply', views.submit_reply, name='submit_reply')

]