from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import menu_view

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', menu_view, name='menu'),  # Single menu path
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Single add-to-cart path
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:product_id>/', views.update_cart_item, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('search/', views.search_results, name='search_results'),
    path('update-dietary-needs/', views.update_dietary_needs, name='update_dietary_needs'),
    path('generate_qr/<int:table_number>/', views.generate_qr, name='generate_qr'),
    path('qr_code/', views.qr_code_page, name='qr_code'),
    path('submit-form/', views.submit_form, name='submit_form'),
]
