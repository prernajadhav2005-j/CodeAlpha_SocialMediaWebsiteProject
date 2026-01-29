from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
import json

from accounts.models import Follow
from .models import Post, Comment, Story
from .forms import PostForm, StoryForm


# 🔄 Redirect root to feed
def feed_redirect(request):
    return redirect("posts:feed")


# ================= FEED =================
@login_required
def feed(request):
    posts = (
        Post.objects
        .select_related("author")
        .order_by("-created")
    )

    stories = (
        Story.objects
        .select_related("user")
        .order_by("-created")
    )

    following_ids = list(
        Follow.objects
        .filter(follower=request.user)
        .values_list("following_id", flat=True)
    )

    return render(request, "posts/feed.html", {
        "posts": posts,
        "stories": stories,
        "following_ids": following_ids,
    })


# ================= CREATE POST (IMAGE + VIDEO) =================
@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)  # Accept image + video
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:feed')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


# ================= CREATE STORY (IMAGE + VIDEO) =================
@login_required
def create_story(request):
    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES)  # Accept image + video
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect('posts:feed')
    else:
        form = StoryForm()
    return render(request, 'posts/create_story.html', {'form': form})


# ================= LIKE / UNLIKE =================
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return JsonResponse({"count": post.likes.count()})


# ================= COMMENTS (AJAX) =================
@login_required
def get_comments(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = post.comment_set.all().order_by("id")
    comments_data = [
        {"username": c.user.username, "text": c.text, "created": c.created.strftime("%H:%M")}
        for c in comments
    ]
    return JsonResponse({"comments": comments_data})


@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        text = request.POST.get("text", "").strip()

        if text == "":
            return JsonResponse({"error": "Comment cannot be empty"}, status=400)

        comment = Comment.objects.create(post=post, user=request.user, text=text)

        return JsonResponse({
            "username": comment.user.username,
            "text": comment.text,
            "created": comment.created.strftime("%H:%M")
        })

    return JsonResponse({"error": "Invalid request"}, status=400)


# ================= DELETE POST =================
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    return redirect("posts:feed")


# ================= EDIT POST =================
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("posts:feed")
    else:
        form = PostForm(instance=post)

    return render(request, "posts/edit_post.html", {"form": form})


# ================= STORY VIEW (JSON + PAGE) =================
@login_required
def view_story_api(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    return JsonResponse({
        "image": story.image.url if story.image else None,
        "video": story.video.url if story.video else None,
        "username": story.user.username
    })


@login_required
def story_page(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    return render(request, 'posts/story_view.html', {'story': story})


# ================= STORIES PAGE =================
@login_required
def stories(request):
    stories = Story.objects.filter(
        created__gte=timezone.now() - timedelta(hours=24)
    )
    return render(request, "posts/stories.html", {"stories": stories})


@login_required
def story_detail(request, pk):
    story = get_object_or_404(Story, pk=pk)
    return JsonResponse({
        "image": story.image.url if story.image else None,
        "video": story.video.url if story.video else None,
        "username": story.user.username
    })
