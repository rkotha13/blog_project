from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'categories', 'media']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }