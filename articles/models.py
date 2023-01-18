from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Book(models.Model):
    book_title = models.CharField(max_length=50)
    img_url = models.TextField(null=True)
    book_content = models.TextField(blank=True)
    book_link = models.TextField(null=True)
    book_genre = models.TextField(null = True)

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    select_book = models.ForeignKey(Book, on_delete=models.PROTECT, null=True)
    content = models.TextField()
    image = models.ImageField(null=False)
    rating = models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    likes = models.ManyToManyField(User, related_name="likes_articles")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    is_private = models.BooleanField(default=False)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


