from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("main:product_list_by_category", args=[self.slug])
    
    @property
    def product_count(self):
        """Return the number of available products in this category."""
        return self.products.filter(available=True).count()


class Product(models.Model):
    category = models.ForeignKey(
        Category, 
        related_name='products',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
            models.Index(fields=['available']),
            models.Index(fields=['category', 'available']),
        ]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.id, self.slug])
    
    @property
    def formatted_price(self):
        """Return formatted price with currency symbol."""
        return f"${self.price}"
    
    def get_related_products(self, limit=4):
        """Get related products from the same category."""
        return Product.objects.filter(
            category=self.category,
            available=True
        ).exclude(id=self.id)[:limit]