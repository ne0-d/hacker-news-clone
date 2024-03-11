from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from .forms import UserCreationForm, LoginForm, SignupForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.contrib.auth.models import User

# Create your views here.
# @login_required(login_url='/login') 
def home(request):
    posts = Post.objects.all()
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
    return redirect('login')

def user_profile(request):
    user = request.user
    comments = Comment.objects.filter(author=user)
    print(comments)
    return render(request, 'profile.html', {'user': user, 'comments': comments})

def user_comments(request, username):
    user = get_object_or_404(User, username=username)
    comments = Comment.objects.filter(author=user)
    return render(request, 'user_comments.html', {'user': user, 'comments': comments})

def submit(request):
    return HttpResponse("Here you can submit your posts but you need to login")

def post(request, post_id):
    return HttpResponse("Post Page %s"% post_id)


