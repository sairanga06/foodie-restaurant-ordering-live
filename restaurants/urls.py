from django.urls import path
from . import views

app_name = "restaurants"
urlpatterns = [
    path("", views.home, name="home"),
    path("restaurant/<slug:slug>/", views.restaurant_detail, name="detail"),
    path("cart/add/<int:item_id>/", views.cart_add, name="cart_add"),
    path("checkout/", views.checkout, name="checkout"),
    path("payment/<int:order_id>/", views.demo_payment, name="demo_payment"),
    path("orders/", views.order_history, name="orders"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("favourite/<slug:slug>/", views.toggle_favourite, name="toggle_favourite"),
    path("restaurant/<slug:slug>/review/", views.add_review, name="add_review"),
    path("area/", views.set_area, name="set_area"),
    path("manager/", views.manager_dashboard, name="manager_dashboard"),
    path("api/restaurants/", views.api_restaurants, name="api_restaurants"),
    path("api/orders/<int:order_id>/status/", views.api_order_status, name="api_order_status"),
]
