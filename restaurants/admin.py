from django.contrib import admin
from .models import Restaurant, MenuItem, Order, Review, Favourite, Coupon, RestaurantManagerProfile

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "delivery_minutes", "is_vegetarian", "is_active")
    list_filter = ("is_vegetarian", "is_featured", "is_active")
    search_fields = ("name", "cuisines", "address")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [MenuItemInline]

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "price", "is_vegetarian", "is_available")
    list_filter = ("is_vegetarian", "is_available")
    search_fields = ("name", "restaurant__name")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "restaurant", "total", "payment_status", "status", "created_at")
    list_filter = ("status", "payment_status", "created_at")
    search_fields = ("customer_name", "phone", "customer__username")
    readonly_fields = ("items_json", "subtotal", "discount", "delivery_fee", "total", "created_at")

admin.site.register(Review)
admin.site.register(Favourite)
admin.site.register(Coupon)
admin.site.register(RestaurantManagerProfile)
