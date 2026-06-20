from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .utils import get_or_create_cart
from catalog.models import ProductVariant
from .models import CartItem
from django.http import JsonResponse

@require_POST
def add_to_cart(request, variant_id):
    cart = get_or_create_cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        variant=variant,
        defaults={"quantity": 1},
    )

    if not created:
        cart_item.quantity +=1
        cart_item.save()
    
    return JsonResponse({"success": True, "total_quantity": cart.total_quantity})

@require_POST
def update_cart_item(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
    quantity = int(request.POST.get("quantity", 1))
    if quantity <= 0:
        cart_item.delete()
        return JsonResponse({"success": True, "total_quantity": cart.total_quantity})
    else:
        cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse({"success": True, "item_total": cart_item.total_price, "cart_total": cart.get_total_price, "total_quantity": cart.total_quantity})
    
@require_POST
def delete_cart_item(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
    cart_item.delete()
    return JsonResponse({"success": True, "total_quantity": cart.total_quantity})

def cart_detail(request):
    cart = get_or_create_cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})