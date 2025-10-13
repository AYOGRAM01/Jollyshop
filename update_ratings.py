import os
import django
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from Mini_catalog.models import Product

def update_product_ratings():
    products = Product.objects.all()
    ratings = [3.0, 3.5, 4.0, 4.5, 5.0]
    for product in products:
        product.rating = random.choice(ratings)
        product.num_ratings = random.randint(10, 100)
        product.save()
        print(f"Updated {product.name} to rating {product.rating}")

if __name__ == '__main__':
    update_product_ratings()
