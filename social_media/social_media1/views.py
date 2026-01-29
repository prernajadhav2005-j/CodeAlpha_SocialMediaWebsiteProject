from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from posts.models import Post

def root_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return redirect('login')

@login_required
def feed_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'feed.html', {'posts': posts})
