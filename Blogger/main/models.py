from django.db import models
from django.utils import timezone

# Create your models here.

class Category(models.Model):
  name = models.CharField(max_length=128)

class Post(models.Model):
  title = models.CharField(max_length=2048)
  content = models.TextField()
  is_published = models.BooleanField(default=True)
  published_at = models.DateField(default =timezone.now)
  post = models.ImageField(upload_to="image/", default="image/default.png")
  categories = models.ManyToManyField(Category)


