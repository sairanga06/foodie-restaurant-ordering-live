import json
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from urllib.parse import urlencode
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Restaurant, MenuItem, Order, Review, Favourite, Coupon, RestaurantManagerProfile

def home(request):
    restaurants = Restaurant.objects.filter(is_active=True).prefetch_related("menu_items", "reviews")
    query = request.GET.get("q", "").strip()
    cuisine = request.GET.get("cuisine", "").strip()
    food_filter = request.GET.get("food", "all").strip().lower()
    if query:
        restaurants = restaurants.filter(
            Q(name__icontains=query) | Q(cuisines__icontains=query) |
            Q(description__icontains=query) | Q(menu_items__name__icontains=query)
        ).distinct()
    if cuisine:
        restaurants = restaurants.filter(cuisines__icontains=cuisine)
    if food_filter == "veg":
        restaurants = restaurants.filter(menu_items__is_vegetarian=True, menu_items__is_available=True).distinct()
    elif food_filter == "nonveg":
        restaurants = restaurants.filter(menu_items__is_vegetarian=False, menu_items__is_available=True).distinct()
    cuisine_options = sorted({
        part.strip() for value in Restaurant.objects.filter(is_active=True).values_list("cuisines", flat=True)
        for part in value.split(",") if part.strip()
    })
    favourite_ids = set(Favourite.objects.filter(user=request.user).values_list("restaurant_id", flat=True)) if request.user.is_authenticated else set()
    return render(request, "restaurants/home.html", {
        "restaurants": restaurants, "query": query, "selected_cuisine": cuisine,
        "selected_food_filter": food_filter, "cuisine_options": cuisine_options,
        "favourite_ids": favourite_ids, "restaurant_count": Restaurant.objects.filter(is_active=True).count(),
        "delivery_area": request.session.get("delivery_area", "Kukatpally"),
    })

def restaurant_detail(request, slug):
    restaurant = get_object_or_404(Restaurant.objects.prefetch_related("menu_items", "reviews__user"), slug=slug, is_active=True)
    is_favourite = request.user.is_authenticated and Favourite.objects.filter(user=request.user, restaurant=restaurant).exists()
    pending_cart_item = None
    if request.user.is_authenticated and request.session.get("pending_cart_item_id"):
        pending = MenuItem.objects.filter(
            pk=request.session["pending_cart_item_id"], restaurant=restaurant, is_available=True
        ).first()
        if pending:
            pending_cart_item = {"id": pending.id, "name": pending.name, "price": pending.price,
                                 "qty": 1, "restaurantId": restaurant.id}
            request.session.pop("pending_cart_item_id", None)
    return render(request, "restaurants/detail.html", {
        "restaurant": restaurant, "is_favourite": is_favourite,
        "pending_cart_item": pending_cart_item,
    })

def _safe_next(request, target):
    if target and url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return target
    return reverse("restaurants:home")

def register(request):
    if request.user.is_authenticated:
        return redirect("restaurants:home")
    next_url = request.POST.get("next") or request.GET.get("next", "")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome! Your demo account is ready.")
        return redirect(_safe_next(request, next_url))
    return render(request, "restaurants/auth.html", {
        "form": form, "page_title": "Create your account", "is_register": True, "next_url": next_url,
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect("restaurants:home")
    next_url = request.POST.get("next") or request.GET.get("next", "")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        messages.success(request, "You are logged in.")
        return redirect(_safe_next(request, next_url))
    return render(request, "restaurants/auth.html", {
        "form": form, "page_title": "Welcome back", "is_register": False, "next_url": next_url,
    })

@require_POST
def cart_add(request, item_id):
    item = get_object_or_404(MenuItem.objects.select_related("restaurant"), pk=item_id, is_available=True, restaurant__is_active=True)
    detail_url = reverse("restaurants:detail", args=[item.restaurant.slug])
    request.session["pending_cart_item_id"] = item.pk
    if not request.user.is_authenticated:
        messages.info(request, "Please log in or create an account first. After login, your selected item will be added to the cart.")
        return redirect(f"{reverse('restaurants:login')}?{urlencode({'next': detail_url})}")
    messages.success(request, f"{item.name} is ready to be added to your cart.")
    return redirect(detail_url)

@require_POST
def logout_view(request):
    logout(request)
    return redirect("restaurants:home")

@login_required
def profile(request):
    return render(request, "restaurants/profile.html", {"favourites": Favourite.objects.filter(user=request.user).select_related("restaurant")})

@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).select_related("restaurant")
    return render(request, "restaurants/orders.html", {"orders": orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.select_related("restaurant"), pk=order_id, customer=request.user)
    stages = ["placed", "confirmed", "preparing", "out_for_delivery", "delivered"]
    active_index = stages.index(order.status) if order.status in stages else -1
    return render(request, "restaurants/order_detail.html", {"order": order, "stages": stages, "active_index": active_index, "clear_cart_on_load": request.GET.get("clear_cart") == "1"})

@login_required
def checkout(request):
    if request.method == "GET":
        return render(request, "restaurants/checkout.html", {"delivery_area": request.session.get("delivery_area", "Kukatpally")})
    customer_name = request.POST.get("customer_name", "").strip()
    phone = request.POST.get("phone", "").strip()
    address = request.POST.get("address", "").strip()
    area = request.POST.get("delivery_area", "Kukatpally").strip()
    coupon_code = request.POST.get("coupon_code", "").strip().upper()
    payment_method = request.POST.get("payment_method", "demo")
    try:
        payload = json.loads(request.POST.get("cart_payload", "[]"))
    except (json.JSONDecodeError, TypeError):
        payload = []
    if not customer_name or not phone or not address or not isinstance(payload, list) or not payload:
        messages.error(request, "Complete the delivery details and add at least one item.")
        return redirect("restaurants:checkout")
    quantities = {}
    for row in payload:
        if isinstance(row, dict):
            try:
                item_id, qty = int(row.get("id")), int(row.get("qty", 0))
                if qty > 0:
                    quantities[item_id] = min(qty, 50)
            except (TypeError, ValueError):
                continue
    items = list(MenuItem.objects.filter(id__in=quantities, is_available=True).select_related("restaurant"))
    if not items:
        messages.error(request, "Your cart is empty or the selected items are unavailable.")
        return redirect("restaurants:checkout")
    if len({item.restaurant_id for item in items}) != 1 or len(items) != len(quantities):
        messages.error(request, "This demo supports one restaurant per order. Please check your cart.")
        return redirect("restaurants:checkout")
    line_items, subtotal = [], 0
    for item in items:
        qty = quantities[item.id]
        line_total = item.price * qty
        subtotal += line_total
        line_items.append({"id": item.id, "name": item.name, "qty": qty, "unit_price": item.price, "line_total": line_total})
    discount = 0
    if coupon_code:
        coupon = Coupon.objects.filter(code__iexact=coupon_code, is_active=True).first()
        if not coupon:
            messages.error(request, "That coupon code is not valid.")
            return redirect("restaurants:checkout")
        if subtotal < coupon.minimum_subtotal:
            messages.error(request, f"This coupon requires a subtotal of ₹{coupon.minimum_subtotal} or more.")
            return redirect("restaurants:checkout")
        discount = int(subtotal * coupon.discount_value / 100) if coupon.discount_type == "percent" else coupon.discount_value
        if coupon.discount_type == "percent":
            discount = min(discount, coupon.max_discount)
        discount = min(discount, subtotal)
    delivery_fee = 30
    total = max(0, subtotal - discount) + delivery_fee
    with transaction.atomic():
        order = Order.objects.create(
            customer=request.user, customer_name=customer_name, phone=phone, address=address,
            delivery_area=area, restaurant=items[0].restaurant, items_json=line_items,
            subtotal=subtotal, discount=discount, delivery_fee=delivery_fee, total=total,
            coupon_code=coupon_code, payment_status="pending",
        )
    # Demo payment only: no payment provider and no card details are collected.
    return redirect("restaurants:demo_payment", order_id=order.pk)

@login_required
def demo_payment(request, order_id):
    order = get_object_or_404(Order, pk=order_id, customer=request.user)
    if request.method == "GET":
        if order.payment_status != "pending":
            return redirect("restaurants:order_detail", order_id=order.pk)
        return render(request, "restaurants/payment.html", {"order": order})
    if request.method != "POST":
        return redirect("restaurants:order_detail", order_id=order.pk)
    result = request.POST.get("result", "success")
    if order.payment_status != "pending":
        return redirect("restaurants:order_detail", order_id=order.pk)
    if result == "success":
        order.payment_status = "success"
        order.status = "confirmed"
        order.save(update_fields=["payment_status", "status"])
        messages.success(request, "Demo payment successful — no real money was charged.")
    else:
        order.payment_status = "failed"
        order.status = "cancelled"
        order.save(update_fields=["payment_status", "status"])
        messages.warning(request, "Demo payment failed. No money was charged.")
    if result == "success":
        return redirect(f"{reverse('restaurants:order_detail', args=[order.pk])}?clear_cart=1")
    return redirect("restaurants:order_detail", order_id=order.pk)

@login_required
@require_POST
def toggle_favourite(request, slug):
    restaurant = get_object_or_404(Restaurant, slug=slug, is_active=True)
    favourite, created = Favourite.objects.get_or_create(user=request.user, restaurant=restaurant)
    if not created:
        favourite.delete()
        messages.info(request, "Removed from favourites.")
    else:
        messages.success(request, "Added to favourites.")
    return redirect(request.POST.get("next") or "restaurants:detail", slug=slug) if request.POST.get("next") == "detail" else redirect("restaurants:home")

@login_required
@require_POST
def add_review(request, slug):
    restaurant = get_object_or_404(Restaurant, slug=slug, is_active=True)
    try:
        rating = int(request.POST.get("rating", "5"))
    except ValueError:
        rating = 5
    comment = request.POST.get("comment", "").strip()
    if rating not in range(1, 6) or not comment:
        messages.error(request, "Choose a rating and write a short review.")
    else:
        Review.objects.update_or_create(user=request.user, restaurant=restaurant, defaults={"rating": rating, "comment": comment[:400]})
        messages.success(request, "Your review was saved.")
    return redirect("restaurants:detail", slug=slug)

@require_POST
def set_area(request):
    allowed = {"Kukatpally", "Balanagar", "Miyapur", "Hitech City", "Ameerpet", "Madhapur"}
    area = request.POST.get("delivery_area", "Kukatpally")
    request.session["delivery_area"] = area if area in allowed else "Kukatpally"
    messages.success(request, f"Demo delivery area set to {request.session['delivery_area']}.")
    return redirect(_safe_next(request, request.POST.get("next")))

@login_required
def manager_dashboard(request):
    profile = RestaurantManagerProfile.objects.filter(user=request.user).select_related("restaurant").first()
    if not (request.user.is_staff or profile):
        return HttpResponseForbidden("A restaurant manager account must be assigned by an administrator.")
    restaurant = profile.restaurant if profile else None
    if request.method == "POST":
        if not restaurant and not request.user.is_superuser:
            return HttpResponseForbidden("No restaurant assigned.")
        action = request.POST.get("action")
        if action == "update_item" and restaurant:
            item = get_object_or_404(MenuItem, pk=request.POST.get("item_id"), restaurant=restaurant)
            item.price = max(0, min(int(request.POST.get("price", item.price)), 100000))
            item.is_available = request.POST.get("is_available") == "on"
            item.save(update_fields=["price", "is_available"])
            messages.success(request, "Menu item updated.")
        elif action == "update_order":
            order = get_object_or_404(Order, pk=request.POST.get("order_id"), restaurant=restaurant) if restaurant else get_object_or_404(Order, pk=request.POST.get("order_id"))
            allowed_statuses = dict(Order.STATUS_CHOICES)
            status = request.POST.get("status")
            if status in allowed_statuses:
                order.status = status
                order.save(update_fields=["status"])
                messages.success(request, "Demo order status updated.")
        return redirect("restaurants:manager_dashboard")
    orders = Order.objects.filter(restaurant=restaurant).select_related("customer") if restaurant else Order.objects.all().select_related("customer")
    menu_items = MenuItem.objects.filter(restaurant=restaurant) if restaurant else MenuItem.objects.all()
    return render(request, "restaurants/manager.html", {"managed_restaurant": restaurant, "orders": orders[:50], "menu_items": menu_items})

def api_restaurants(request):
    rows = Restaurant.objects.filter(is_active=True).values("id", "name", "slug", "cuisines", "rating", "delivery_minutes", "cost_for_two")
    return JsonResponse({"count": len(rows), "results": list(rows)})

def api_order_status(request, order_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "authentication_required"}, status=401)
    order = get_object_or_404(Order, pk=order_id, customer=request.user)
    return JsonResponse({"order_id": order.id, "status": order.status, "payment_status": order.payment_status, "updated_at": order.created_at.isoformat()})
