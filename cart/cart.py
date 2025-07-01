from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from main.models import Product
from decimal import Decimal


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, override_quantity=False):
        """Add a product to the cart or update its quantity."""
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
                'name': product.name
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
            
        # Ensure quantity doesn't exceed reasonable limits
        if self.cart[product_id]['quantity'] > 99:
            self.cart[product_id]['quantity'] = 99
            
        self.save()

    def save(self):
        """Mark the session as modified to save changes."""
        self.session.modified = True

    def remove(self, product):
        """Remove a product from the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Iterate over the items in the cart and get the related Product objects."""
        product_ids = self.cart.keys()
        # Optimize query with select_related
        products = Product.objects.filter(id__in=product_ids).select_related('category')
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Return the total number of items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())
    
    def __contains__(self, product):
        """Check if a product is in the cart."""
        return str(product.id) in self.cart
        
    def get_total_price(self):
        """Calculate the total cost of the items in the cart."""
        return sum(
            Decimal(item['price']) * item['quantity'] 
            for item in self.cart.values()
        )
    
    def get_item_count(self):
        """Get the number of different items in the cart."""
        return len(self.cart)
    
    def get_product_quantity(self, product):
        """Get the quantity of a specific product in the cart."""
        product_id = str(product.id)
        return self.cart.get(product_id, {}).get('quantity', 0)
    
    def update_quantity(self, product, quantity):
        """Update the quantity of a product in the cart."""
        if quantity <= 0:
            self.remove(product)
        else:
            self.add(product, quantity, override_quantity=True)
    
    def clear(self):
        """Remove the cart from session."""
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
    def is_empty(self):
        """Check if the cart is empty."""
        return len(self.cart) == 0
    
    def get_cart_items(self):
        """Get all cart items with product objects."""
        return list(self.__iter__())
    
    def get_formatted_total(self):
        """Get formatted total price with currency symbol."""
        return f"${self.get_total_price():.2f}"

    