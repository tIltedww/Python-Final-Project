from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 1. ЖАНРЫ (Они независимы)
class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название жанра")
    image = models.ImageField(upload_to='genres/', blank=True, null=True, verbose_name="Обложка жанра")

    def __str__(self):
        return self.name

# 2. КНИГИ (Они ссылаются на Жанр)
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='books')
    rating = models.FloatField()
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    cover = models.ImageField(upload_to='covers/', default='covers/default_book.png', blank=True)

    def __str__(self):
        return self.title

# 3. ПРОФИЛЬ (Он ссылается на Книгу)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    # Теперь Book уже определен выше, и ошибки не будет
    favorite_books = models.ManyToManyField(Book, blank=True, related_name='favorited_by')

    def __str__(self):
        return f'Профиль {self.user.username}'

# СИГНАЛЫ (Всегда внизу)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()