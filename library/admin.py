from django.contrib import admin
from .models import Book, Profile, Genre

# 1. Регистрация Жанров
admin.site.register(Genre)

# 2. Регистрация Профилей
admin.site.register(Profile)

# 3. Регистрация Книг (ИСПОЛЬЗУЕМ ТОЛЬКО ОДИН СПОСОБ)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'rating')
    search_fields = ('title', 'author')
    list_filter = ('genre', 'rating')