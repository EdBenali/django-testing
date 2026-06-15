from django.db import models
from django.utils import timezone


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    published_at = models.DateTimeField("date published", default=timezone.now)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title
