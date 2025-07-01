from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import Http404
from .models import Category, Product
from cart.forms import CartAddProductForm


class ProductListView(ListView):
    model = Product
    template_name = 'main/product/list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        """Optimize queries with select_related and filter by availability."""
        queryset = Product.objects.filter(available=True).select_related('category')
        
        # Filter by category if slug is provided
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)
        else:
            self.category = None
            
        # Apply sorting
        sort_by = self.request.GET.get('sort')
        if sort_by:
            if sort_by == 'name':
                queryset = queryset.order_by('name')
            elif sort_by == '-name':
                queryset = queryset.order_by('-name')
            elif sort_by == 'price':
                queryset = queryset.order_by('price')
            elif sort_by == '-price':
                queryset = queryset.order_by('-price')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add categories and category context to template."""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category'] = self.category
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product/detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        """Optimize query and ensure product is available."""
        return Product.objects.filter(available=True).select_related('category')
    
    def get_object(self, queryset=None):
        """Get product by id and slug, with better error handling."""
        try:
            product = get_object_or_404(
                self.get_queryset(),
                id=self.kwargs['id'],
                slug=self.kwargs['slug']
            )
            return product
        except (KeyError, ValueError):
            raise Http404("Product not found")
    
    def get_context_data(self, **kwargs):
        """Add related products and cart form to context."""
        context = super().get_context_data(**kwargs)
        context['related_products'] = self.object.get_related_products()
        context['cart_product_form'] = CartAddProductForm()
        return context


# Legacy function-based views for backward compatibility
def product_list(request, category_slug=None):
    """Legacy function-based view - redirects to class-based view."""
    view = ProductListView.as_view()
    return view(request, category_slug=category_slug)


def product_detail(request, id, slug):
    """Legacy function-based view - redirects to class-based view."""
    view = ProductDetailView.as_view()
    return view(request, id=id, slug=slug)