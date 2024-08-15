from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.template.defaultfilters import slugify

from taggit.managers import TaggableManager

from app_account.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_list', blank=True, null=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=False, null=False, unique=True)
    body = models.TextField()
    cover = models.ImageField(upload_to='images/', default='default.jpg')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("app_blog:blog_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, null=True)
    body = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("app_blog:blog_detail", kwargs={"slug": self.slug})
