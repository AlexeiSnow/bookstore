from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Book, Category, Order


def book_list(request):
    books = Book.objects.filter(is_available=True)
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    author = request.GET.get('author')
    year = request.GET.get('year')
    sort = request.GET.get('sort')

    if category_id:
        books = books.filter(category_id=category_id)
    if author:
        books = books.filter(author__icontains=author)
    if year:
        books = books.filter(year=year)

    if sort == 'author':
        books = books.order_by('author')
    elif sort == 'year':
        books = books.order_by('year')
    elif sort == 'price':
        books = books.order_by('buy_price')
    else:
        books = books.order_by('title')

    return render(request, 'books/book_list.html', {
        'books': books,
        'categories': categories,
        'selected_category': category_id,
        'selected_sort': sort,
    })


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})


@login_required
def create_order(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        order_type = request.POST.get('order_type')

        if order_type == Order.RENT_2W:
            expires_at = timezone.now() + timedelta(weeks=2)
        elif order_type == Order.RENT_1M:
            expires_at = timezone.now() + timedelta(days=30)
        elif order_type == Order.RENT_3M:
            expires_at = timezone.now() + timedelta(days=90)
        else:
            expires_at = None  # покупка — без срока

        Order.objects.create(
            user=request.user,
            book=book,
            order_type=order_type,
            expires_at=expires_at,
        )
        return redirect('my_orders')

    return render(request, 'books/order_form.html', {'book': book})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'books/my_orders.html', {'orders': orders})