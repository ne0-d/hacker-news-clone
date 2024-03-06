from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Home Page contains list of posts by users!")

def login(request):
    return HttpResponse("Login page of user")

def register(request):
    return HttpResponse("Register Page of user")

def profile(request):
    return HttpResponse("User profile page")

def submit(request):
    return HttpResponse("Here you can submit your posts but you need to login")

def post(request, post_id):
    return HttpResponse("Post Page %s"% post_id)


