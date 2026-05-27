from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('order/<int:pk>/', views.create_order, name='create_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
]