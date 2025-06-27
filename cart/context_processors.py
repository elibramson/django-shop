from main.models import Product

def cart_processor(request):
    cart = request.session.get('cart', {})
    cart_items = []
    cart_count = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            cart_items.append({
                'product': product,
                'quantity': quantity
            })
            cart_count += quantity
        except Product.DoesNotExist:
            continue
    
    return {
        'cart': cart_items,
        'cart_count': cart_count
    } 