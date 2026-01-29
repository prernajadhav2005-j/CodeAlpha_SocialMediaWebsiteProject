from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)  # Video field
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created = models.DateTimeField(auto_now_add=True)  # FIXED

    def __str__(self):
        return f"{self.author.username} - {self.created}"


class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stories/', blank=True, null=True)
    video = models.FileField(upload_to='stories/videos/', blank=True, null=True)  # Video field
    created = models.DateTimeField(auto_now_add=True)  # FIXED

    def __str__(self):
        return f"{self.user.username} - {self.created}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)  # FIXED

    def __str__(self):
        return f"{self.user.username} - {self.text[:20]}"