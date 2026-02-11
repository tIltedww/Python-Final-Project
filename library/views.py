from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, Profile, Genre
from .forms import UserUpdateForm, ProfileUpdateForm

# 1. ГЛАВНАЯ СТРАНИЦА
def home(request):
    return render(request, 'library/home.html')

# 2. РЕГИСТРАЦИЯ
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# 3. ЛИЧНЫЙ КАБИНЕТ (ПРОФИЛЬ)
@login_required
def profile(request):
    # Гарантируем наличие профиля
    profile_obj, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Ваш профиль был обновлен!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'library/profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })

# 4. СПИСОК ЖАНРОВ (Это будет первая страница при нажатии на "Книги")
@login_required
def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'library/genre_list.html', {'genres': genres})



# 5. КНИГИ КОНКРЕТНОГО ЖАНРА
@login_required
def books_by_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(genre=genre, title__icontains=query)
    else:
        books = Book.objects.filter(genre=genre)
    
    return render(request, 'library/book_list.html', {
        'genre': genre, 
        'books': books
    })

# 6. ДЕТАЛЬНАЯ СТРАНИЦА КНИГИ (Обложка слева, инфо справа)
@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'library/book_detail.html', {'book': book})

# 7. ДОБАВЛЕНИЕ/УДАЛЕНИЕ ИЗ ИЗБРАННОГО
@login_required
def add_to_favorites(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    profile = request.user.profile
    if book in profile.favorite_books.all():
        profile.favorite_books.remove(book)
        messages.info(request, f'Книга "{book.title}" удалена из избранного.')
    else:
        profile.favorite_books.add(book)
        messages.success(request, f'Книга "{book.title}" добавлена в избранное!')
    return redirect('book_detail', book_id=book.id)

# 8. РЕСУРСЫ (Если есть такая страница)
def resources(request):
    return render(request, 'library/resources.html')

def all_books_search(request):
    query = request.GET.get('q')
    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books, 'search_mode': True})