from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, library

class ProductForm(forms.ModelForm):
    price = forms.CharField(
        label='Price (₦)',
        widget=forms.TextInput(attrs={'placeholder': 'Enter price (e.g., 1,000)'}),
        help_text='Enter price with commas if needed (e.g., 1,000)'
    )

    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'in_stock', 'image', 'discount_percentage']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Format the price with commas for display
            self.fields['price'].initial = f"{self.instance.price:,.2f}"

    def clean_price(self):
        price = self.cleaned_data['price']
        # Remove commas and convert to float
        try:
            cleaned_price = float(price.replace(',', ''))
            if cleaned_price < 0:
                raise forms.ValidationError("Price cannot be negative.")
            return cleaned_price
        except ValueError:
            raise forms.ValidationError("Enter a valid price (e.g., 1000 or 1,000).")

class AdminUserCreationForm(UserCreationForm):
    is_staff = forms.BooleanField(
        required=False,
        label="Create as Admin",
        help_text="Check this box to create an admin user with full access to the system."
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "is_staff")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_staff = self.cleaned_data["is_staff"]
        if user.is_staff:
            user.is_superuser = True  # Make admin users superusers too
        if commit:
            user.save()
        return user

class LibraryForm(forms.ModelForm):
    class Meta:
        model = library
        fields = ['title', 'description', 'imagee']

