from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from main.models import Product

# Create your views here.

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            item_total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total += item_total
        except Product.DoesNotExist:
            continue
    
    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total': total
    })

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1
    
    request.session['cart'] = cart
    messages.success(request, f'{product.name} added to cart.')
    
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, 'Item removed from cart.')
    
    return redirect('cart:cart_detail')
