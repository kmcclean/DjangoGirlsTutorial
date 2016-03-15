from django import forms

from .models import Post

# This creates a form that will allow users to post to the blog.
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
