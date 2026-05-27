from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    author = models.CharField(max_length=200, verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    year = models.IntegerField(verbose_name='Год написания')
    description = models.TextField(verbose_name='Описание')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name='Обложка')
    buy_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена покупки')
    rent_price_2w = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Аренда 2 недели')
    rent_price_1m = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Аренда 1 месяц')
    rent_price_3m = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Аренда 3 месяца')
    is_available = models.BooleanField(default=True, verbose_name='Доступна')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f'{self.title} — {self.author}'


class Order(models.Model):
    PURCHASE = 'buy'
    RENT_2W = 'rent_2w'
    RENT_1M = 'rent_1m'
    RENT_3M = 'rent_3m'

    ORDER_TYPES = [
        (PURCHASE, 'Покупка'),
        (RENT_2W, 'Аренда 2 недели'),
        (RENT_1M, 'Аренда 1 месяц'),
        (RENT_3M, 'Аренда 3 месяца'),
    ]

    STATUS_ACTIVE = 'active'
    STATUS_EXPIRED = 'expired'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Активен'),
        (STATUS_EXPIRED, 'Истёк'),
        (STATUS_COMPLETED, 'Завершён'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    order_type = models.CharField(max_length=10, choices=ORDER_TYPES, verbose_name='Тип')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE, verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата окончания')
    notified = models.BooleanField(default=False, verbose_name='Уведомление отправлено')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.user} — {self.book} ({self.get_order_type_display()})'