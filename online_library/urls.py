from django.contrib import admin
from django.urls import path, include
from library import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    
    path('books/', views.genre_list, name='genre_list'),
    path('genre/<int:genre_id>/', views.books_by_genre, name='books_by_genre'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    
    path('add-favorite/<int:book_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('resources/', views.resources, name='resources'),
    path('search/', views.all_books_search, name='all_books_search'),
]

# Это критически важная часть для работы аватарок и обложек книг:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)