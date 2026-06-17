from django.contrib import admin
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Book, Category, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'year', 'buy_price', 'is_available']
    list_filter = ['category', 'is_available', 'year']
    search_fields = ['title', 'author']
    list_editable = ['buy_price', 'is_available']
    ordering = ['title']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'order_type', 'status', 'created_at', 'expires_at', 'notified']
    list_filter = ['status', 'order_type']
    search_fields = ['user__username', 'book__title']
    list_editable = ['status']
    actions = ['send_expiry_reminder']

    def send_expiry_reminder(self, request, queryset):
        sent = 0
        for order in queryset:
            if order.expires_at and order.status == Order.STATUS_ACTIVE:
                days_left = (order.expires_at - timezone.now()).days
                send_mail(
                    subject='Напоминание об аренде книги',
                    message=f'Здравствуйте, {order.user.username}!\n\n'
                            f'Срок аренды книги "{order.book.title}" '
                            f'истекает через {days_left} дн. ({order.expires_at.strftime("%d.%m.%Y")}).\n\n'
                            f'С уважением, Книжный магазин',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[order.user.email],
                    fail_silently=True,
                )
                order.notified = True
                order.save()
                sent += 1
        self.message_user(request, f'Отправлено напоминаний: {sent}')

    send_expiry_reminder.short_description = 'Отправить напоминание об окончании аренды'