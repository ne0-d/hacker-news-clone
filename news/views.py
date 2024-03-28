from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import (
    UserCreationForm,
    LoginForm,
    SignupForm,
    PostForm,
    CommentForm,
    EditComment,
)
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count
from django.conf import settings
from django.urls import reverse


def create_pagination(request, obj_list, per_page):
    p = Paginator(obj_list, per_page)
    page_number = request.GET.get("page")
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    return page_obj


def home(request):
    posts = (
        Post.objects.annotate(flag_count=Count("flagged_by_users"))
        .prefetch_related("flagged_by_users")
        .select_related("author")
        .filter(flag_count__lt=settings.MIN_FLAG_COUNT)
        .order_by("-pubDate")
    )

    # posts = Post.objects.annotate(flag_count=Count('flagged_by_users')).annotate(comment_count=Count('comment')).prefetch_related('flagged_by_users').select_related('author').filter(flag_count__lt=settings.MIN_FLAG_COUNT)

    for post in posts:
        print("Flag count: ", post.flag_count)
        # print('Comment count: ', post.comment_count)
        post.is_flagged_by_user = request.user in post.flagged_by_users.all()

    page_obj = create_pagination(request, posts, 5)
    context = {
        "page_obj": page_obj,
        "MIN_FLAG_COUNT": settings.MIN_FLAG_COUNT,
    }
    return render(request, "index.html", context)


def user_login(request):
    print("get next: ", request.GET.get("next", ""))
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                next_url = request.POST.get("next", "")
                if not next_url:
                    next_url = request.GET.get("next", "")
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect("home")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        next_url = request.GET.get("next")
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


def user_logout(request):
    print("in logout")
    logout(request)
    return redirect("home")


def general_profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "general_profile.html", {"user": user})


def user_comments(request, username):
    user = get_object_or_404(User, username=username)
    comments = Comment.objects.filter(author=user).order_by("-pubDate")
    comments_dict = [get_comment_dict(comment) for comment in comments]
    page_obj = create_pagination(request, comments_dict, 10)
    return render(
        request,
        "user_comments.html",
        {"user": user, "comments": comments, "page_obj": page_obj},
    )


def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = (
        Post.objects.annotate(flag_count=Count("flagged_by_users"))
        .prefetch_related("flagged_by_users")
        .select_related("author")
        .filter(author=user)
        .order_by("-pubDate")
    )
    for post in posts:
        post.is_flagged_by_user = request.user in post.flagged_by_users.all()

    page_obj = create_pagination(request, posts, 10)
    print(settings.ALLOWED_EDIT_SECONDS)
    return render(
        request,
        "user_posts.html",
        {
            "user": user,
            "page_obj": page_obj,
            "ALLOWED_EDIT_SECONDS": settings.ALLOWED_EDIT_SECONDS,
            "MIN_FLAG_COUNT": settings.MIN_FLAG_COUNT,
        },
    )


def get_comment_dict(comment):
    comment_data = {
        "id": comment.id,
        "author": comment.author.id,
        "username": comment.author.username,
        "text": comment.text,
        "pubDate": comment.pubDate,
        "lastUpdated": comment.lastUpdated,
        
    }
    if comment.child_count == 0:
        comment_data['child_comments'] = []
    else:
        comment_data['child_comments'] = [
            get_comment_dict(child)
            for child in comment.comment_set.select_related("author").annotate(child_count=Count("comment"))
            .all()
            .order_by("-pubDate")
        ]
    return comment_data


def post_comments(request, post_id):
    print("Next URL: ", request.get_full_path())
    post = get_object_or_404(Post, id=post_id)
    comments = (
        Comment.objects.select_related("author")
        .filter(post=post, parentComment__isnull=True).annotate(child_count=Count("comment"))
        .order_by("-pubDate")
    )
    comments_dict = [get_comment_dict(comment) for comment in comments]
    page_obj = create_pagination(request, comments_dict, 10)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.pubDate = timezone.now()
                comment.save()
                next_url = request.GET.get("next", None)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(
                        reverse("post_comments", kwargs={"post_id": post_id})
                    )
            else:
                messages.error(request, "You need to login to comment")
                return redirect(reverse("login") + "?next=" + request.path)
    else:
        form = CommentForm()
    return render(
        request,
        "post_comments.html",
        {
            "post": post,
            "page_obj": page_obj,
            "form": form,
            "ALLOWED_EDIT_SECONDS": settings.ALLOWED_EDIT_SECONDS,
        },
    )


@login_required(login_url="/login")
def submit_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pubDate = timezone.now()
            post.save()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "submit_post.html", {"form": form})


@login_required(login_url="/login")
def submit_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parentComment = parent_comment
            reply.post = parent_comment.post
            reply.pubDate = timezone.now()
            reply.save()
            return redirect("post_comments", post_id=parent_comment.post.id)
    else:
        form = CommentForm()
    return render(
        request, "submit_reply.html", {"parent_comment": parent_comment, "form": form}
    )


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        if request.method == "POST":
            form = EditComment(request.POST, instance=comment)
            if form.is_valid():
                comment.lastUpdated = timezone.now()
                form.save()
                messages.success(request, "Comment updated successfully")
                return redirect("post_comments", post_id=comment.post.id)
        else:
            form = EditComment(instance=comment)
        return render(request, "edit_comment.html", {"form": form, "comment": comment})
    else:
        messages.error(request, "You are not authorized to edit this comment")
        return redirect("post_comments", post_id=comment.post.id)


@login_required
def toggle_flag_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if user in post.flagged_by_users.all():
        post.flagged_by_users.remove(user)
    else:
        post.flagged_by_users.add(user)
    return redirect("home")
