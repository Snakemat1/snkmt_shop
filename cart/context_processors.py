from .utils import get_or_create_cart

def cart_total_quantity(request):
    cart = get_or_create_cart(request)
    return {"cart_total_quantity": cart.total_quantity}