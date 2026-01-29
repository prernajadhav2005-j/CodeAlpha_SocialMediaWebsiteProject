from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.feed, name="feed"),
    path("create-post/", views.create_post, name="create_post"),
    path("create-story/", views.create_story, name="create_story"),
    path("toggle-like/<int:post_id>/", views.toggle_like, name="toggle_like"),
    path("add-comment/<int:post_id>/", views.add_comment, name="add_comment"),
    path("get_comments/<int:pk>/", views.get_comments, name="get_comments"),
    path("edit/<int:post_id>/", views.edit_post, name="edit_post"),
    path("delete/<int:post_id>/", views.delete_post, name="delete_post"),
    path("story/<int:story_id>/", views.story_page, name="story_view"),
    path("story/api/<int:story_id>/", views.view_story_api, name="story_api"),
    path("stories/", views.stories, name="stories"),

    path("story/<int:pk>/", views.story_detail, name="story_detail"),
]