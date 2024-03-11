from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    url = models.TextField()
    pubDate = models.DateTimeField("published_date")

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=250) 
    pubDate = models.DateTimeField("published_date")
    parentComment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)