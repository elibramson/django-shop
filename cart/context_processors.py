from .cart import Cart

def cart(request):
    """Context processor to make cart available in all templates."""
    cart_instance = Cart(request)
    return {
        'cart': cart_instance,
        'cart_count': len(cart_instance),
        'cart_total': cart_instance.get_formatted_total(),
        'is_cart_empty': cart_instance.is_empty(),
    }
