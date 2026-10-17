# Initial schema for the Foodie demo project.
# Generated-style migration committed so production deploys can run `migrate` safely.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("slug", models.SlugField(blank=True, max_length=50, unique=True)),
                ("cuisines", models.CharField(help_text="Comma-separated cuisines", max_length=220)),
                ("description", models.TextField(blank=True)),
                ("address", models.CharField(default="Hyderabad, Telangana", max_length=220)),
                ("image_url", models.URLField(blank=True)),
                ("rating", models.DecimalField(decimal_places=1, default=4.0, max_digits=2)),
                ("delivery_minutes", models.PositiveSmallIntegerField(default=30)),
                ("cost_for_two", models.PositiveIntegerField(default=400)),
                ("is_vegetarian", models.BooleanField(default=False)),
                ("is_featured", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-is_featured", "-rating", "name"]},
        ),
        migrations.CreateModel(
            name="Coupon",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=30, unique=True)),
                ("description", models.CharField(max_length=180)),
                ("discount_type", models.CharField(choices=[("percent", "Percentage"), ("fixed", "Fixed amount")], max_length=10)),
                ("discount_value", models.PositiveIntegerField()),
                ("minimum_subtotal", models.PositiveIntegerField(default=0)),
                ("max_discount", models.PositiveIntegerField(default=100)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="MenuItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("description", models.CharField(blank=True, max_length=240)),
                ("price", models.PositiveIntegerField()),
                ("is_vegetarian", models.BooleanField(default=True)),
                ("is_available", models.BooleanField(default=True)),
                ("restaurant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="menu_items", to="restaurants.restaurant")),
            ],
            options={"ordering": ["price", "name"]},
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("customer_name", models.CharField(max_length=120)),
                ("phone", models.CharField(max_length=20)),
                ("address", models.TextField()),
                ("delivery_area", models.CharField(default="Kukatpally", max_length=100)),
                ("items_json", models.JSONField(default=list)),
                ("subtotal", models.PositiveIntegerField(default=0)),
                ("discount", models.PositiveIntegerField(default=0)),
                ("delivery_fee", models.PositiveIntegerField(default=30)),
                ("total", models.PositiveIntegerField(default=0)),
                ("coupon_code", models.CharField(blank=True, max_length=30)),
                ("payment_status", models.CharField(choices=[("pending", "Pending"), ("success", "Demo payment successful"), ("failed", "Demo payment failed")], default="pending", max_length=12)),
                ("status", models.CharField(choices=[("placed", "Order placed"), ("confirmed", "Confirmed"), ("preparing", "Preparing"), ("out_for_delivery", "Out for delivery"), ("delivered", "Delivered"), ("cancelled", "Cancelled")], default="placed", max_length=24)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("customer", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="foodie_orders", to=settings.AUTH_USER_MODEL)),
                ("restaurant", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="restaurants.restaurant")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rating", models.PositiveSmallIntegerField(choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")])),
                ("comment", models.CharField(max_length=400)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("restaurant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="restaurants.restaurant")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Favourite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("restaurant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favourited_by", to="restaurants.restaurant")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="RestaurantManagerProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("restaurant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="managers", to="restaurants.restaurant")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="restaurant_manager_profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name="review",
            constraint=models.UniqueConstraint(fields=("user", "restaurant"), name="one_review_per_user_restaurant"),
        ),
        migrations.AddConstraint(
            model_name="favourite",
            constraint=models.UniqueConstraint(fields=("user", "restaurant"), name="one_favourite_per_user_restaurant"),
        ),
    ]
