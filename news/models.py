from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    url = models.TextField()
    pubDate = models.DateTimeField("published_date", default=timezone.localtime(timezone.now()))
    flagged_by_users = models.ManyToManyField(User, related_name='flagged_posts', blank=True)
    def flag_count(self):
        return self.flagged_by_users.count()
    def get_absolute_url(self):
        return reverse('post_comments', args=[str(self.id)])
   

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField() 
    pubDate = models.DateTimeField("published_date", default=timezone.localtime(timezone.now()))
    lastUpdated = models.DateTimeField("last_updated", null=True, blank=True)
    parentComment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.text + "->" + self.author.username
    