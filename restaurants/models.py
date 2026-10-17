from django.conf import settings
from django.db import models
from django.utils.text import slugify

class Restaurant(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    cuisines = models.CharField(max_length=220, help_text="Comma-separated cuisines")
    description = models.TextField(blank=True)
    address = models.CharField(max_length=220, default="Hyderabad, Telangana")
    image_url = models.URLField(blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.0)
    delivery_minutes = models.PositiveSmallIntegerField(default=30)
    cost_for_two = models.PositiveIntegerField(default=400)
    is_vegetarian = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-is_featured", "-rating", "name"]
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name="menu_items", on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=240, blank=True)
    price = models.PositiveIntegerField()
    is_vegetarian = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    class Meta:
        ordering = ["price", "name"]
    def __str__(self):
        return f"{self.name} — {self.restaurant.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ("placed", "Order placed"), ("confirmed", "Confirmed"), ("preparing", "Preparing"),
        ("out_for_delivery", "Out for delivery"), ("delivered", "Delivered"), ("cancelled", "Cancelled"),
    ]
    PAYMENT_CHOICES = [("pending", "Pending"), ("success", "Demo payment successful"), ("failed", "Demo payment failed")]
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="foodie_orders")
    customer_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    delivery_area = models.CharField(max_length=100, default="Kukatpally")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    items_json = models.JSONField(default=list)
    subtotal = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    delivery_fee = models.PositiveIntegerField(default=30)
    total = models.PositiveIntegerField(default=0)
    coupon_code = models.CharField(max_length=30, blank=True)
    payment_status = models.CharField(max_length=12, choices=PAYMENT_CHOICES, default="pending")
    status = models.CharField(max_length=24, choices=STATUS_CHOICES, default="placed")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return f"Order #{self.pk} — {self.customer_name}"

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name="reviews", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(n, str(n)) for n in range(1, 6)])
    comment = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["user", "restaurant"], name="one_review_per_user_restaurant")]
    def __str__(self):
        return f"{self.rating}/5 — {self.restaurant.name}"

class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name="favourited_by", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "restaurant"], name="one_favourite_per_user_restaurant")]
    def __str__(self):
        return f"{self.user} ♥ {self.restaurant}"

class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=180)
    discount_type = models.CharField(max_length=10, choices=[("percent", "Percentage"), ("fixed", "Fixed amount")])
    discount_value = models.PositiveIntegerField()
    minimum_subtotal = models.PositiveIntegerField(default=0)
    max_discount = models.PositiveIntegerField(default=100)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.code

class RestaurantManagerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="restaurant_manager_profile")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="managers")
    def __str__(self):
        return f"{self.user.username} manages {self.restaurant.name}"
