from django.core.management.base import BaseCommand
from Mini_catalog.models import library

class Command(BaseCommand):
    help = 'Add sample images to the carousel library'

    def handle(self, *args, **options):
        # Sample carousel images - using placeholder URLs that can be replaced with actual images
        sample_images = [
            {
                'title': 'Welcome to JollyShop',
                'description': 'Your one-stop shop for amazing products',
                'imagee': 'https://via.placeholder.com/800x300/667eea/ffffff?text=Welcome+to+JollyShop'
            },
            {
                'title': 'Amazing Discounts',
                'description': 'Up to 80% off on selected items',
                'imagee': 'https://via.placeholder.com/800x300/ff6b6b/ffffff?text=Amazing+Discounts'
            },
            {
                'title': 'Quality Products',
                'description': 'Premium quality guaranteed',
                'imagee': 'https://via.placeholder.com/800x300/4ecdc4/ffffff?text=Quality+Products'
            },
            {
                'title': 'Fast Delivery',
                'description': 'Quick and reliable shipping',
                'imagee': 'https://via.placeholder.com/800x300/45b7d1/ffffff?text=Fast+Delivery'
            },
            {
                'title': 'Customer Satisfaction',
                'description': 'Your satisfaction is our priority',
                'imagee': 'https://via.placeholder.com/800x300/f9ca24/ffffff?text=Customer+Satisfaction'
            },
            {
                'title': 'New Arrivals',
                'description': 'Discover the latest trending products',
                'imagee': 'https://via.placeholder.com/800x300/9b59b6/ffffff?text=New+Arrivals'
            },
            {
                'title': 'Free Shipping',
                'description': 'Free delivery on orders over ₦50',
                'imagee': 'https://via.placeholder.com/800x300/1abc9c/ffffff?text=Free+Shipping'
            },
            {
                'title': 'Exclusive Deals',
                'description': 'Members-only special offers',
                'imagee': 'https://via.placeholder.com/800x300/e74c3c/ffffff?text=Exclusive+Deals'
            },
            {
                'title': 'Best Sellers',
                'description': 'Most popular products loved by customers',
                'imagee': 'https://via.placeholder.com/800x300/f39c12/ffffff?text=Best+Sellers'
            },
            {
                'title': 'Shop Now',
                'description': 'Browse our extensive collection today',
                'imagee': 'https://via.placeholder.com/800x300/3498db/ffffff?text=Shop+Now'
            }
        ]

        for image_data in sample_images:
            # Check if image with this title already exists
            if not library.objects.filter(title=image_data['title']).exists():
                library.objects.create(**image_data)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added carousel image: "{image_data["title"]}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Carousel image "{image_data["title"]}" already exists')
                )

        total_images = library.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'Total carousel images in database: {total_images}')
        )
