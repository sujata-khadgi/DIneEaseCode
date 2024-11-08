from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),  # Custom login view
    path('logout/', views.user_logout, name='logout'),
    path('cart/', views.get_cart_items, name='cart'),  # Cart page
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),  # Add to cart
    path('search/', views.search_results, name='search_results'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('menu/', views.menu, name='menu'),  # Menu page
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='cart_login'),  # Default login view
]



  
