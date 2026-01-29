from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import SignupForm, LoginForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile, Follow, Notification
from posts.models import Post

# =========================
# 🔐 LOGIN
# =========================
def login_view(request):
    if request.user.is_authenticated:
        return redirect('posts:feed')  # change to your feed view

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next') or 'posts:feed'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


# =========================
# 🆕 SIGNUP
# =========================
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data.get("password")
            user.set_password(raw_password)
            user.save()

            # ⛔ FIX: check if profile already exists
            profile, created = Profile.objects.get_or_create(user=user)

            # Save uploaded images
            if form.cleaned_data.get("profile_image"):
                profile.image = form.cleaned_data["profile_image"]

            if form.cleaned_data.get("cover_image"):
                profile.cover = form.cleaned_data["cover_image"]

            profile.save()

            login(request, user)
            return redirect("posts:feed")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


# =========================
# 🚪 LOGOUT
# =========================
@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


# =========================
# 🔑 SIMPLE FORGOT PASSWORD (USERNAME RESET)
# =========================
def forgot_password(request):
    """
    Simple password reset:
    User enters username, new password, confirm password.
    Password is updated directly if username exists and passwords match.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Check that all fields are filled
        if not username or not new_password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect("accounts:forgot_password")

        # Check that passwords match
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("accounts:forgot_password")

        # Try to update password
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successful. Please login.")
            return redirect("accounts:login")
        except User.DoesNotExist:
            messages.error(request, "Username not found.")
            return redirect("accounts:forgot_password")

    return render(request, "accounts/forgot_password.html")


# =========================
# 👤 PROFILE
# =========================
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by("-created")

    following_ids = set()
    if request.user.is_authenticated:
        following_ids = set(
            Follow.objects.filter(follower=request.user)
            .values_list("following_id", flat=True)
        )

    return render(request, "accounts/profile.html", {
        "profile_user": profile_user,
        "posts": posts,
        "following_ids": following_ids,
    })


# =========================
# 🔍 USER SEARCH
# =========================
@login_required
def user_search(request):
    q = request.GET.get("q", "")
    users = User.objects.filter(username__icontains=q).exclude(id=request.user.id)
    following_ids = set(
        Follow.objects.filter(follower=request.user)
        .values_list("following_id", flat=True)
    )
    return render(request, "accounts/user_search.html", {
        "users": users,
        "following_ids": following_ids
    })


# =========================
# ✏️ EDIT PROFILE
# =========================
@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profile)

    return render(request, "accounts/edit_profile.html", {
        "u_form": u_form,
        "p_form": p_form,
    })

@login_required
def delete_account(request):
    user = request.user 

    user.delete()

    messages.success(request, "Your account has been permanently deleted.")
    return redirect("accounts:login")

# =========================
# 🔔 NOTIFICATIONS
# =========================
@login_required
def notifications(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, "accounts/notifications.html", {
        "users": users
    })


# =========================
# ➕ TOGGLE FOLLOW (AJAX)
# =========================
@login_required
@csrf_exempt
def toggle_follow(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    data = json.loads(request.body)
    user_id = data.get("user_id")

    target_user = get_object_or_404(User, id=user_id)

    if target_user == request.user:
        return JsonResponse({"error": "Cannot follow yourself"}, status=400)

    follow_obj = Follow.objects.filter(
        follower=request.user,
        following=target_user
    )

    if follow_obj.exists():
        follow_obj.delete()
        status = "unfollowed"
    else:
        Follow.objects.create(
            follower=request.user,
            following=target_user
        )
        status = "followed"

    followers_count = Follow.objects.filter(following=target_user).count()

    return JsonResponse({
        "status": status,
        "followers_count": followers_count
    })


# =========================
# FOLLOWERS LIST
# =========================
@login_required
def followers_view(request, username):
    user = get_object_or_404(User, username=username)
    followers = Follow.objects.filter(following=user)
    return render(request, "accounts/followers.html", {
        "profile_user": user,
        "followers": followers,
    })


# =========================
# FOLLOWING LIST
# =========================
@login_required
def following_view(request, username):
    user = get_object_or_404(User, username=username)
    following = Follow.objects.filter(follower=user)
    return render(request, "accounts/following.html", {
        "profile_user": user,
        "following": following,
    })
