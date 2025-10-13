from django.shortcuts import render, redirect, get_object_or_404
from .models import library
from .models import Category, Product, Cart, CartItem, Order, OrderItem, ContactMessage, CompletedOrder, RejectedOrder, InboxMessage, Wishlist, WishlistItem
from .forms import ProductForm, AdminUserCreationForm, LibraryForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout

def product_list(request):

    # Imports all the photos and save it in the database

    photo = library.objects.all()

    cloudinary_img = {'photo':photo}

    # Ensure only Luxury and Affordable categories exist
    Category.objects.get_or_create(name='Luxury')
    Category.objects.get_or_create(name='Affordable')
    # Remove any unwanted categories
    Category.objects.exclude(name__in=['Luxury', 'Affordable']).delete()

    categories = Category.objects.all()
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search = request.GET.get('search')

    products = Product.objects.all()
    if category_id:
        if category_id.isdigit():
            products = products.filter(category_id=int(category_id))
        elif category_id == 'affordable':
            products = products.filter(price__lt=50)
        elif category_id == 'luxury':
            products = products.filter(price__gt=200)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if search:
        products = products.filter(name__icontains=search) | products.filter(description__icontains=search)

    return render(request, "home.html", {
        "photo": photo,
        "products": products,
        "categories": categories,
        "selected_category": category_id,
        "min_price": min_price,
        "max_price": max_price,
        "search": search,
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_product(request):
    # Ensure only Luxury and Affordable categories exist
    Category.objects.get_or_create(name='Luxury')
    Category.objects.get_or_create(name='Affordable')
    # Remove any unwanted categories
    Category.objects.exclude(name__in=['Luxury', 'Affordable']).delete()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('product_list')

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all fields.')

    return render(request, 'contact.html')

def register(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = AdminUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'{product.name} added to cart!')
    return redirect('product_list')

@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        items = cart.cartitem_set.all()
        total = sum(item.total_price() for item in items)
    else:
        items = []
        total = 0
    return render(request, 'cart.html', {'items': items, 'total': total})

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.cartitem_set.exists():
        messages.warning(request, "Your cart is empty. Add items before checking out.")
        return redirect('view_cart')

    items = cart.cartitem_set.all()
    total = sum(item.total_price() for item in items)

    if request.method == 'POST':
        # Process the checkout
        delivery_address = request.POST.get('delivery_address')
        proof_of_payment = request.FILES.get('proof_of_payment')

        if not delivery_address:
            messages.error(request, 'Please provide a delivery address.')
            return redirect('checkout')

        if not proof_of_payment:
            messages.error(request, 'Please upload proof of payment.')
            return redirect('checkout')

        # Create the order with pending status
        order = Order.objects.create(
            user=request.user,
            status='pending',
            total_amount=total,
            delivery_address=delivery_address,
            proof_of_payment=proof_of_payment
        )

        # Create order items from cart items
        for cart_item in items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price  # Store current price
            )

        # Clear the cart
        cart.cartitem_set.all().delete()

        messages.success(request, f'Order #{order.id} has been submitted for approval! Your cart has been cleared.')
        return redirect('order_history')

    # Render checkout page with payment details
    return render(request, 'checkout.html', {
        'items': items,
        'total': total,
        'account_number': '0123456789',
        'bank_name': 'GTBank',
        'account_name': 'JollyShop Nigeria Ltd'
    })

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('view_cart')

@login_required
def increase_quantity(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.quantity += 1
        item.save()
        messages.success(request, f'Quantity of {item.product.name} increased!')
    return redirect('view_cart')

@login_required
def decrease_quantity(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
            messages.success(request, f'Quantity of {item.product.name} decreased!')
        else:
            messages.warning(request, 'Cannot decrease quantity below 1. Use remove instead.')
    return redirect('view_cart')

# New admin dashboard view
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    users = User.objects.all()
    total_users = users.count()
    total_orders = Order.objects.filter(status='completed').count()
    total_products = Product.objects.count()
    carousel_images = library.objects.all()

    if request.method == 'POST':
        form = LibraryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Carousel image added successfully!')
            return redirect('admin_dashboard')
    else:
        form = LibraryForm()

    return render(request, 'admin_dashboard.html', {
        'users': users,
        'total_users': total_users,
        'total_orders': total_orders,
        'total_products': total_products,
        'carousel_images': carousel_images,
        'form': form,
    })

# New order management view
@login_required
@user_passes_test(lambda u: u.is_staff)
def order_management(request):
    orders = Order.objects.all().order_by('-created_at').prefetch_related('items__product', 'user')
    return render(request, 'order_management.html', {
        'orders': orders,
    })

from django.core.mail import send_mail
from django.conf import settings

from django.utils import timezone

@login_required
@user_passes_test(lambda u: u.is_staff)
def approve_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == 'pending':
        order.status = 'approved'
        order.save()

        # Create inbox message for the user
        from datetime import timedelta
        delivery_date = timezone.now() + timedelta(days=3)
        inbox_subject = f"Order #{order.id} Approved - Delivery Scheduled"
        inbox_message = f"Hello {order.user.username},\n\nYour order #{order.id} has been approved! Your package will be delivered within 3 days (by {delivery_date.strftime('%B %d, %Y')}).\n\nDelivery Address:\n{order.delivery_address}\n\nThank you for shopping with us!"

        InboxMessage.objects.create(
            user=order.user,
            subject=inbox_subject,
            message=inbox_message,
            message_type='order_update'
        )

        # Send email to user about approval and delivery address
        user_email = order.user.email
        email_subject = f"Your Order #{order.id} has been Approved"
        email_message = f"Hello {order.user.username},\n\nYour order #{order.id} has been approved. Please wait for delivery at the following address:\n\n{order.delivery_address}\n\nThank you for shopping with us!"
        send_mail(email_subject, email_message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=True)

        messages.success(request, f'Order #{order.id} has been approved and user notified!')
    return redirect('order_management')

@login_required
@user_passes_test(lambda u: u.is_staff)
def reject_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == 'pending':
        order.status = 'rejected'
        order.save()
        # Move to RejectedOrder table
        from .models import RejectedOrder
        RejectedOrder.objects.create(
            original_order_id=order.id,
            user=order.user,
            created_at=order.created_at,
            rejected_at=timezone.now(),
            total_amount=order.total_amount,
            delivery_address=order.delivery_address,
            proof_of_payment=order.proof_of_payment,
            rejection_reason="Rejected by admin"
        )
        order.delete()
        messages.success(request, f'Order #{order.id} has been rejected and archived!')
    return redirect('order_management')

@login_required
@user_passes_test(lambda u: u.is_staff)
def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == 'approved':
        order.status = 'completed'
        order.save()
        # Move to CompletedOrder table
        from .models import CompletedOrder
        CompletedOrder.objects.create(
            original_order_id=order.id,
            user=order.user,
            created_at=order.created_at,
            completed_at=timezone.now(),
            total_amount=order.total_amount,
            delivery_address=order.delivery_address,
            proof_of_payment=order.proof_of_payment
        )
        order.delete()
        messages.success(request, f'Order #{order_id} has been marked as completed and archived!')
    return redirect('order_management')

# New contact messages view
@login_required
@user_passes_test(lambda u: u.is_staff)
def completed_orders(request):
    completed_orders = CompletedOrder.objects.all().order_by('-completed_at').prefetch_related('user')
    return render(request, 'completed_orders.html', {
        'completed_orders': completed_orders,
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def rejected_orders(request):
    rejected_orders = RejectedOrder.objects.all().order_by('-rejected_at').prefetch_related('user')
    return render(request, 'rejected_orders.html', {
        'rejected_orders': rejected_orders,
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def contact_messages(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'contact_messages.html', {
        'messages': messages_list,
    })

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).exclude(status='pending').order_by('-created_at').prefetch_related('items__product')
    return render(request, 'order_history.html', {
        'orders': orders,
    })

@login_required
def inbox(request):
    messages_list = InboxMessage.objects.filter(user=request.user).order_by('-created_at')
    unread_count = messages_list.filter(is_read=False).count()

    # Mark messages as read when viewed
    if request.method == 'POST':
        message_id = request.POST.get('mark_read')
        if message_id:
            message = get_object_or_404(InboxMessage, id=message_id, user=request.user)
            message.is_read = True
            message.save()

    return render(request, 'inbox.html', {
        'messages': messages_list,
        'unread_count': unread_count,
    })

def logout_view(request):
    if request.method in ['GET', 'POST']:
        auth_logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('register')
    return redirect('product_list')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

@login_required
def view_wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    items = wishlist.wishlistitem_set.all()
    return render(request, 'wishlist.html', {'items': items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_item, created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
    if not created:
        messages.info(request, f'{product.name} is already in your wishlist!')
    else:
        messages.success(request, f'{product.name} added to wishlist!')
    return redirect('product_list')

@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)
    item.delete()
    messages.success(request, 'Item removed from wishlist!')
    return redirect('view_wishlist')

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_carousel_image(request, image_id):
    image = get_object_or_404(library, id=image_id)
    image.delete()
    messages.success(request, 'Carousel image deleted successfully!')
    return redirect('admin_dashboard')
