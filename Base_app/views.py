from django.shortcuts import render,redirect,get_object_or_404
from .models import New_arrival,Featured_product,CustomUser,CartItem,Earphone , Headphone , TechGadget , Address , AllProduct
from django.contrib.auth import login, authenticate, logout 
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from Base_app.models import CartItem, New_arrival, Featured_product
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.views.decorators.http import require_POST
from .forms import AddressForm
from django.db.models import Q


# Create your views here.
def homepage(request):
    products = Featured_product.objects.all().order_by('-created_at')
    newarrivalproduct =  New_arrival.objects.all().order_by('-created_at')
    return render(request, 'homepage/home.html',  {'products': products, 'newarrivalproduct': newarrivalproduct})

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Hash password
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "authentication/register.html", {"form": form})

# ✅ Login View
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect("homepage")  # Redirect to homepage
        messages.error(request, "Invalid email or password.")
    
    form = LoginForm()
    return render(request, "authentication/login.html", {"form": form})

# ✅ Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("homepage")

@login_required
@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_id = data.get("product_id", "").strip()
            product_type = data.get("product_type", "").strip()

            if not product_id or not product_type:
                return JsonResponse({"success": False, "message": "Invalid product data"}, status=400)

            user = request.user

            if product_type == "new_arrival":
                product = New_arrival.objects.filter(id=product_id).first()
                if not product:
                    return JsonResponse({"success": False, "message": "New Arrival product not found"}, status=404)
                cart_item, created = CartItem.objects.get_or_create(
                    user=user, new_arrival=product, defaults={"quantity": 1, "product_type": "new_arrival"}
                )

            elif product_type == "featured_product":
                product = Featured_product.objects.filter(id=product_id).first()
                if not product:
                    return JsonResponse({"success": False, "message": "Featured product not found"}, status=404)
                cart_item, created = CartItem.objects.get_or_create(
                    user=user, featured_product=product, defaults={"quantity": 1, "product_type": "featured_product"}
                )

            elif product_type == "earphone":
                product = Earphone.objects.filter(id=product_id).first()
                if not product:
                    return JsonResponse({"success": False, "message": "Earphone product not found"}, status=404)
                cart_item, created = CartItem.objects.get_or_create(
                    user=user, earphone=product, defaults={"quantity": 1, "product_type": "earphone"}
                )

            elif product_type == "headphone":
                product = Headphone.objects.filter(id=product_id).first()
                if not product:
                    return JsonResponse({"success": False, "message": "Headphone product not found"}, status=404)
                cart_item, created = CartItem.objects.get_or_create(
                    user=user, headphone=product, defaults={"quantity": 1, "product_type": "headphone"}
                )

            elif product_type == "techgadget":
                product = TechGadget.objects.filter(id=product_id).first()
                if not product:
                    return JsonResponse({"success": False, "message": "Tech Gadget not found"}, status=404)
                cart_item, created = CartItem.objects.get_or_create(
                    user=user, techgadget=product, defaults={"quantity": 1, "product_type": "techgadget"}
                )

            else:
                return JsonResponse({"success": False, "message": "Invalid product type"}, status=400)

            if not created:
                cart_item.quantity += 1
                cart_item.save()

            return JsonResponse({"success": True, "message": "Item added to cart"})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data"}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)



@login_required
def cart_count(request):
    user_cart = CartItem.objects.filter(user=request.user)
    cart_item_count = user_cart.count()
    return JsonResponse({"success": True, "count": cart_item_count})


def cart_context(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    return {"cart_count": cart_count}


@login_required
def cart_view(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user).select_related(
        'new_arrival', 'featured_product', 'earphone', 'headphone', 'techgadget'
    )

    for item in cart_items:
        if item.product_type == 'new_arrival' and item.new_arrival:
            item.item_total = item.new_arrival.price * item.quantity
        elif item.product_type == 'featured_product' and item.featured_product:
            item.item_total = item.featured_product.price * item.quantity
        elif item.product_type == 'earphone' and item.earphone:
            item.item_total = item.earphone.price * item.quantity
        elif item.product_type == 'headphone' and item.headphone:
            item.item_total = item.headphone.price * item.quantity
        elif item.product_type == 'techgadget' and item.techgadget:
            item.item_total = item.techgadget.price * item.quantity
        else:
            item.item_total = Decimal('0.00')

    subtotal = sum(item.item_total for item in cart_items)
    tax_rate = Decimal('0.08')
    tax = subtotal * tax_rate
    total = subtotal + tax

    return render(request, 'cartpage/cartpage.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total
    })




@login_required
@csrf_exempt
def remove_from_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            item_id = data.get("item_id")

            cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
            cart_item.delete()

            cart_items = CartItem.objects.filter(user=request.user)
            subtotal = sum(
                item.new_arrival.price * item.quantity if item.product_type == "new_arrival" and item.new_arrival
                else item.featured_product.price * item.quantity if item.product_type == "featured_product" and item.featured_product
                else item.earphone.price * item.quantity if item.product_type == "earphone" and item.earphone
                else item.headphone.price * item.quantity if item.product_type == "headphone" and item.headphone
                else item.techgadget.price * item.quantity if item.product_type == "techgadget" and item.techgadget
                else 0
                for item in cart_items
            )

            tax_rate = Decimal("0.08")
            tax = subtotal * tax_rate
            total = subtotal + tax

            return JsonResponse({
                "success": True,
                "message": "Item removed",
                "cart_count": cart_items.count(),
                "subtotal": float(subtotal),
                "tax": float(tax),
                "total": float(total),
            })

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)


def earphone_list(request):
    earphones = Earphone.objects.all().order_by('-created_at')
    return render(request, 'earphone/earphone.html', {'earphones': earphones})

def headphone_list(request):
    headphones = Headphone.objects.all()
    return render(request, 'headphone/headphone.html', {'headphones': headphones})

def techgadget_list_view(request):
    gadgets = TechGadget.objects.all()
    return render(request, 'techgadget/techgadget.html', {'gadgets': gadgets})


def new_arrival_detail(request, pk):
    product = get_object_or_404(New_arrival, pk=pk)
    return render(request, 'Description_page/new_arrival_detail.html', {
        'product': product,
        'product_type': 'new_arrival'
    })

def featured_product_detail(request, pk):
    product = get_object_or_404(Featured_product, pk=pk)
    return render(request, 'Description_page/featured_product_detail.html', {
        'product': product,
        'product_type': 'featured_product'
    })

def earphone_detail(request, pk):
    product = get_object_or_404(Earphone, pk=pk)
    return render(request, 'Description_page/earphone_detail.html', {
        'product': product,
        'product_type': 'earphone'
    })

def headphone_detail(request, pk):
    product = get_object_or_404(Headphone, pk=pk)
    return render(request, 'Description_page/headphone_detail.html', {
        'product': product,
        'product_type': 'headphone'
    })

def techgadget_detail(request, pk):
    product = get_object_or_404(TechGadget, pk=pk)
    return render(request, 'Description_page/techgadget_detail.html', {
        'product': product,
        'product_type': 'techgadget'
    })

    
@login_required
def add_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect("show_address")  # or your order page
    else:
        form = AddressForm()
    return render(request, "addresspage/addresspage.html", {"form": form})

@login_required
def show_address(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'addresspage/showaddress.html', {'addresses': addresses})

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == 'POST':
        address.delete()
    return redirect('show_address')

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('show_address')
    else:
        form = AddressForm(instance=address)

    return render(request, 'addresspage/edit.html', {'form': form})


def checkout_view(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)

    # Fetch cart items for the logged-in user
    cart_items = CartItem.objects.filter(user=request.user)

    # Calculate subtotal, tax, and total
    subtotal = 0
    for item in cart_items:
        if item.product_type == 'new_arrival' and item.new_arrival:
            subtotal += item.new_arrival.price * item.quantity
        elif item.product_type == 'featured_product' and item.featured_product:
            subtotal += item.featured_product.price * item.quantity
        elif item.product_type == 'earphone' and item.earphone:
            subtotal += item.earphone.price * item.quantity
        elif item.product_type == 'headphone' and item.headphone:
            subtotal += item.headphone.price * item.quantity
        elif item.product_type == 'techgadget' and item.techgadget:
            subtotal += item.techgadget.price * item.quantity

    tax = round(Decimal(subtotal) * Decimal('0.08'), 2)
    total = round(Decimal(subtotal) + tax, 2)

    context = {
        'address': address,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
    }
    return render(request, 'Checkout _page/checkout.html', context)

def new_navbar(request):
    return render(request, 'homepage/navbar1.html')
