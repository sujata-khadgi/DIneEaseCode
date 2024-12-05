from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Product, CartItems
import qrcode
from django.http import HttpResponse
from io import BytesIO
import json

def home(request):
    category_filter = request.GET.get('category', 'all')  # Default to 'all' if no category is selected
    menu_products = Product.objects.all()  # Get all products

    # Filter by category if specified (excluding 'all' category)
    if category_filter != 'all':
        menu_products = menu_products.filter(category=category_filter)

    featured_products = Product.objects.filter(is_featured=True)  # Featured products

    return render(request, 'home.html', {
        'featured_products': featured_products,
        'menu_products': menu_products,
    })
def menu(request):
    # Retrieve menu items for the menu page
    menu_items = Product.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})


def about(request):
    # Static about page
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


@login_required(login_url='login')
def cart(request):
    cart_items = CartItems.objects.filter(user=request.user)
    print(cart_items)  # Check if cart items exist for the user
    cart_products = []

    for item in cart_items:
        print(f"Product: {item.product.name}, Quantity: {item.quantity}")  # Debugging: Print product name and quantity

        product = item.product  # Access the associated product
        cart_products.append({
            'product': product,
            'quantity': item.quantity,
            'subtotal': item.product.price * item.quantity,
        })

    total_price = sum(item['subtotal'] for item in cart_products)
    dietary_needs = request.session.get('dietary_needs', '')

    return render(request, 'cart.html', {
        'cart_products': cart_products,
        'total_price': total_price,
        'dietary_needs': dietary_needs,
    })

@csrf_exempt  # For simplicity; in production, use CSRF tokens
def submit_form(request):
    if request.method == 'POST':
        # Parse the received data
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')

        # Simulate some processing
        if name and email:
            response = {
                'status': 'success',
                'message': f"Form received. Name: {name}, Email: {email}"
            }
        else:
            response = {
                'status': 'error',
                'message': 'Invalid data provided.'
            }

        return JsonResponse(response)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@csrf_exempt
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItems.objects.get_or_create(
        user=request.user, 
        product=product
    )
    if not created:
        cart_item.quantity += 1  # Increase quantity if product already exists
    cart_item.save()
    return redirect('cart')

@login_required(login_url='login')
def remove_from_cart(request, product_id):
    # Remove a product from the cart
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]  # Remove the product from the cart
        request.session['cart'] = cart  # Save the updated cart to session
        messages.success(request, "Item removed from cart.")
    else:
        messages.error(request, "Item not found in cart.")
    return redirect('cart')


@login_required(login_url='login')
def update_cart_item(request, product_id):
    # Update the quantity of an item in the cart
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] = quantity  # Update the quantity
            request.session['cart'] = cart  # Save the updated cart to session
            messages.success(request, "Cart updated successfully.")
        else:
            messages.error(request, "Item not found in cart.")
    return redirect('cart')


@login_required(login_url='login')
def checkout(request):
    # Process the checkout
    cart_items = CartItems.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    total_bill = sum(item.product.price * item.quantity for item in cart_items)

    # Optionally clear the cart after checkout
    cart_items.delete()

    return render(request, 'thank_you.html', {'total_bill': total_bill})


def search_results(request):
    query = request.GET.get('query', '')
    results = Product.objects.filter(name__icontains=query)
    context = {
        'query': query,
        'results': results
    }
    return render(request, 'search_results.html', context)


def update_dietary_needs(request):
    # Update the dietary preferences in the session
    if request.method == "POST":
        dietary_needs = request.POST.get("dietary_needs", "")
        request.session["dietary_needs"] = dietary_needs
        messages.success(request, "Dietary preferences updated successfully!")
    return redirect('cart')


# Generate QR Code
def generate_qr(request, table_number):
    # URL for login page
    login_url = 'http://127.0.0.1:8000/accounts/login/'

    # Generate the QR code with the login URL
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=5,
    )
    qr.add_data(login_url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return HttpResponse(img_io, content_type='image/png')


def qr_code_page(request):
    # Example list of table numbers
    table_numbers = [1, 2, 3, 4, 5]
    return render(request, 'qr_code.html', {'table_numbers': table_numbers})

def menu_view(request):
    menu_items = MenuItem.objects.filter(available=True)
    return render(request, 'menu.html', {'menu_items': menu_items})