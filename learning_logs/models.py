from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from autoslug import AutoSlugField
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.conf import settings


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Topic(models.Model):
    text = models.CharField(max_length=250)
    body = models.TextField(blank=True)
    slug = AutoSlugField(populate_from='text', max_length=250, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)
    updated = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='topic_liked', blank=True)
    total_likes = models.PositiveIntegerField(default=0)
    total_views = models.PositiveIntegerField(default=0)
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-date_added']
        indexes = [
            models.Index(fields=['-date_added']),
            models.Index(fields=['-total_likes']),
        ]

    def get_absolute_url(self):
        return reverse('learning_logs:topic', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.text)
        super().save(*args, **kwargs)



    def __str__(self):
        """Return a string representation of a model"""
        return self.text


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, related_name='entries', on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']
        indexes = [
            models.Index(fields=['-date_added']),
        ]

    def __str__(self):
        return f'{self.text[:50]}...'
