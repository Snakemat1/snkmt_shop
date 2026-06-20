from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("add/<int:variant_id>/", views.add_to_cart, name="add"),
    path("update/<int:item_id>/", views.update_cart_item, name="update"),
    path("delete/<int:item_id>/", views.delete_cart_item, name="delete"),
    path("", views.cart_detail, name="detail")
]
