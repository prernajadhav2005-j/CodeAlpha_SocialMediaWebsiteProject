from django import forms
from .models import Post, Story


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'video']  # ✅ Added video field
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "What's on your mind?",
                'rows': 2
            })
        }


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['image', 'video']  # ✅ Added video field
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control-file'})  # ✅ Added video widget
        }
