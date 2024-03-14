from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from .forms import UserCreationForm, LoginForm, SignupForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect


def home(request):
    posts = Post.objects.all().order_by('-pubDate')
    return render(request, 'index.html', {'posts': posts})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def user_profile(request):
    user = request.user
    comments = Comment.objects.filter(author=user).order_by('-pubDate')
    print(comments)
    return render(request, 'profile.html', {'user': user, 'comments': comments})


def general_profile(request, username):
    user = get_object_or_404(User, username=username)
    comments = Comment.objects.filter(author=user).order_by('-pubDate')
    return render(request, 'general_profile.html', {'user': user, 'comments': comments})


def user_comments(request, username):
    user = get_object_or_404(User, username=username)
    comments = Comment.objects.select_related('author').filter(author=user).order_by('-pubDate')
    comments_dict = [get_comment_dict(comment) for comment in comments]
    return render(request, 'user_comments.html', {'user': user, 'comments': comments, 'comments_dict': comments_dict})


def get_comment_dict(comment):
    return {
        'id':comment.id,
        'author':comment.author.id,
        'username': comment.author.username,
        'text':comment.text,
        'pubDate':comment.pubDate,
        'child_comments': [get_comment_dict(child) for child in comment.comment_set.select_related('author').all().order_by('-pubDate')]
    }


def post_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.select_related('author').filter(post=post, parentComment__isnull=True).order_by('-pubDate')
    comments_dict = [get_comment_dict(comment) for comment in comments]
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                return HttpResponseRedirect(request.path_info)
            else:
                messages.error(request, 'You need to login to comment')
                return redirect('login')
    else:
        form = CommentForm()
    return render(request, 'post_comments.html', {'post': post, 'comments_dict': comments_dict, 'form': form})


@login_required(login_url='/login')
def submit_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'submit_post.html', {'form': form})


@login_required(login_url='/login')
def submit_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parentComment = parent_comment
            reply.post = parent_comment.post
            reply.save()
            return redirect('post_comments', post_id = parent_comment.post.id)
    else:
        form = CommentForm()
    return render(request, 'submit_reply.html', {'parent_comment': parent_comment, 'form':form})




