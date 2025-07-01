from django.shortcuts import render, redirect, \
    get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    """Add a product to the cart."""
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id, available=True)
        form = CartAddProductForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            cart.add(
                product=product, 
                quantity=cd['quantity'],
                override_quantity=cd['override']
            )
            messages.success(request, f'{product.name} added to cart successfully!')
        else:
            messages.error(request, 'Invalid quantity. Please try again.')
            
    except Exception as e:
        messages.error(request, 'An error occurred while adding to cart.')
        
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """Remove a product from the cart."""
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        messages.success(request, f'{product.name} removed from cart.')
    except Exception as e:
        messages.error(request, 'An error occurred while removing from cart.')
        
    return redirect('cart:cart_detail')


def cart_detail(request):
    """Display the cart contents."""
    cart = Cart(request)
    
    # Add update forms for each cart item
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True,
        })
    
    context = {
        'cart': cart,
        'cart_total': cart.get_formatted_total(),
        'item_count': cart.get_item_count(),
        'is_empty': cart.is_empty(),
    }
    
    return render(request, 'cart/cart_detail.html', context)


@require_POST
def cart_update(request, product_id):
    """Update the quantity of a product in the cart."""
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id, available=True)
        form = CartAddProductForm(request.POST)
        
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart.update_quantity(product, quantity)
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'cart_total': cart.get_formatted_total(),
                    'item_count': len(cart),
                    'product_total': f"${(product.price * quantity):.2f}"
                })
            else:
                messages.success(request, f'{product.name} quantity updated.')
        else:
            messages.error(request, 'Invalid quantity.')
            
    except Exception as e:
        messages.error(request, 'An error occurred while updating cart.')
        
    return redirect('cart:cart_detail')


def cart_clear(request):
    """Clear all items from the cart."""
    if request.method == 'POST':
        cart = Cart(request)
        cart.clear()
        messages.success(request, 'Cart cleared successfully.')
        
    return redirect('cart:cart_detail')