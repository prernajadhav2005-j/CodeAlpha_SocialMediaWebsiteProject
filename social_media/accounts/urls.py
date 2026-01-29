from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [

    # 🔐 Authentication
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
  

    # 👤 Profile
    path("profile/<str:username>/", views.profile_view, name="profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("delete-account/", views.delete_account, name="delete_account"),

    path("toggle-follow/", views.toggle_follow, name="toggle_follow"),
   # path('followers/', views.followers_list, name='followers'),
    #path('following/', views.following_list, name='following'),
    path("followers/<str:username>/", views.followers_view, name="followers"),
    path("following/<str:username>/", views.following_view, name="following"),
    path("search/", views.user_search, name="user_search"),
    path("notifications/", views.notifications, name="notifications"),
]

