from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from .models import Order


@shared_task
def check_expiring_rentals():
    """Отправляет напоминания за 3 дня до окончания аренды"""
    now = timezone.now()
    warning_date = now + timedelta(days=3)

    # Находим заказы которые истекают через 3 дня
    expiring_orders = Order.objects.filter(
        status=Order.STATUS_ACTIVE,
        expires_at__date=warning_date.date(),
        notified=False,
    )

    sent = 0
    for order in expiring_orders:
        if order.user.email:
            send_mail(
                subject='Напоминание об аренде книги',
                message=(
                    f'Здравствуйте, {order.user.username}!\n\n'
                    f'Срок аренды книги "{order.book.title}" '
                    f'истекает {order.expires_at.strftime("%d.%m.%Y")}.\n\n'
                    f'Успейте продлить аренду или вернуть книгу.\n\n'
                    f'С уважением, Книжный магазин'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.user.email],
                fail_silently=True,
            )
            order.notified = True
            order.save()
            sent += 1

    return f'Отправлено напоминаний: {sent}'


@shared_task
def update_expired_orders():
    """Автоматически помечает просроченные заказы"""
    now = timezone.now()

    expired_count = Order.objects.filter(
        status=Order.STATUS_ACTIVE,
        expires_at__lt=now,
    ).update(status=Order.STATUS_EXPIRED)

    return f'Обновлено просроченных заказов: {expired_count}'