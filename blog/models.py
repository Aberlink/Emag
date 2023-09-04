from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article")
    published = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    objects = models.Manager()

    class Meta:
        ordering = ("-published",)

    def __str__(self):
        return f"{self.title} || {self.author} || {self.published}"
