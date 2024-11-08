from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from account.models import Product, CartItems
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def menu(request):
    menu_items = Product.objects.all()  # Adjust to filter or group items as needed
    return render(request, 'menu.html', {'menu_items': menu_items})

def about(request):
    return render(request, 'about.html')

def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data["password1"]
        user.set_password(password)
        user.customer = True
        user.save()
        messages.success(request, "Registration successful. You can now log in.")
        return redirect("login")
    return render(request, 'account/register.html', {'form1': form})

def user_login(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["email"],
            password=form.cleaned_data["password"]
        )
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')  # Default to 'home' if 'next' is not provided
            return redirect(next_url)
    return render(request, 'account/login.html', {'form1': form})

def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")

@login_required(login_url='login')  # Ensuring redirection to the login page if not logged in
def get_cart_items(request):
    cart_products = CartItems.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_products)
    return render(request, 'cart.html', {'cart_products': cart_products, 'total_price': total_price})

@csrf_exempt
@login_required(login_url='login')  # Ensuring only logged-in users can access
def cart(request):
    return render(request, 'cart.html')

@login_required(login_url='login')  # Enforcing login for add-to-cart functionality
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_name = data.get('product_name')
        quantity = int(data.get('quantity', 1))

        product = get_object_or_404(Product, name=product_name)
        cart_item, created = CartItems.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return JsonResponse({'message': f'{quantity} of {product_name} added to cart'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def update_cart_item(request, item_id):
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        cart_item = CartItems.objects.get(id=item_id)
        cart_item.quantity = quantity
        cart_item.save()
    return redirect('cart')

def checkout(request):
    return render(request, 'checkout.html')

def search_results(request):
    query = request.GET.get('query', '')
    results = Product.objects.filter(name__icontains=query)
    context = {
        'query': query,
        'results': results
    }
    return render(request, 'search_results.html', context)
