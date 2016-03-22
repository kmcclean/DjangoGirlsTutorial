from django.shortcuts import render
from django.utils import timezone
from .models import Post, Comment
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# This is because I forgot to say how far I am with the lab and need something
# to upload a new commit.
# Create your views here.
# Views is the same as the Controller in the Model-Controller-View setup.

# This gets the list of posts. This also functions at the main page of the website.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

# This gets the details of a give post. When a post is selected this opens up the
# full file to be shown in the browser.
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# This creates a new post. It takes the information from the templates, and puts
# it into a new blog entry, if the information is correct.
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

# This gets the edit information from the templates, and if the information is correct,
# passes it to the models. It then redirects you to the edited blog entry page.
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# This shows a list of all the drafted posts that have not be published yet.
@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

# This function actually publishes the post once it has been approved.
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.author = request.user
    post.publish()
    return redirect('blog.views.post_detail', pk=pk)

#This function removes posts that have been selected to be deleted.
@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.author = request.user
    post.delete()
    return redirect('blog.views.post_list')

# This adds comments to individual posts.
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

#This will approve comments that have been made on the blog.
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog.views.post_detail', pk=comment.post.pk)

# This will delete comments that have been made on the blog.
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog.views.post_detail', pk=post_pk)
