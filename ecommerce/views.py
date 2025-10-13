from django.shortcuts import render

def product_list(request):
    # For now, fake products (until we connect DB)
    products = [
        {"name": "Phone", "price": 250, "description": "Latest Android phone", "image_url": "https://via.placeholder.com/200", "in_stock": True},
        {"name": "Laptop", "price": 800, "description": "Fast and lightweight", "image_url": "https://via.placeholder.com/200", "in_stock": False},
    ]
    return render(request, "Mini_catalog/index.html", {"products": products})