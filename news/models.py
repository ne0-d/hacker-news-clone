from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    url = models.TextField()
    pubDate = models.DateTimeField("published_date", default=timezone.now())

    def get_absolute_url(self):
        return reverse('post_comments', args=[str(self.id)])
   

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField() 
    pubDate = models.DateTimeField("published_date", default=timezone.now())
    parentComment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.text + "->" + self.author.username
    