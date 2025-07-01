from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1, 
        max_value=99, 
        initial=1,
        validators=[
            MinValueValidator(1, message="Quantity must be at least 1."),
            MaxValueValidator(99, message="Quantity cannot exceed 99.")
        ],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '99',
            'style': 'width: 80px;'
        })
    )
    override = forms.BooleanField(
        required=False, 
        initial=False, 
        widget=forms.HiddenInput
    )
    
    def clean_quantity(self):
        """Additional validation for quantity."""
        quantity = self.cleaned_data.get('quantity')
        if quantity and quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")
        return quantity
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add help text for better UX
        self.fields['quantity'].help_text = "Enter quantity (1-99)"
    