from django.contrib.auth.models import AbstractUser
from django.db import models
    
    
class User(AbstractUser):
    has_followers = models.IntegerField(default=0, blank=True)
    following = models.ManyToManyField('Following', related_name="following", blank=True)
    
    def __str__(self):
        return f"Profile: {self.username}, followers: {self.has_followers}, following: {self.following.count()}"
    

class Post(models.Model):
    username = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField()
    likes = models.IntegerField(default=0, blank=True)
    is_liked = models.BooleanField(default=False, blank=True)
    
    def __str__(self):
        return f"{self.id} {self.username}"
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} likes {self.post}"
    
    
class Following(models.Model):
    username = models.CharField(max_length=255)
    
    

    

