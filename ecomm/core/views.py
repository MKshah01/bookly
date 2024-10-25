from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg , Count
from core.forms import ProductReviewForm
from core.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address




# Create your views here.

def index(request):
    # You can add context data here if needed
    products = Product.objects.filter()  # Fixed filter syntax
    context = {
        "products": products,  # Updated context to use the correct variable
    }

    return render(request, 'core/index.html', context)  # Fixed render parameters


def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products,
        
    }
    return render(request, 'core/product-list.html', context)


def category_list(request):
    categories = Category.objects.all()  # Fetch all categories
    category_count = categories.count()  # Count the number of categories
    context = {
        'categories': categories,  # Use the correct variable name
        'category_count': category_count,  # Add category count to context
    }
    return render(request, 'core/category.html', context) 


def category_product_list_view(request, cid):

    # Get the category based on the cid
    category = get_object_or_404(Category, cid=cid)  # Fixed syntax for fetching category

    
    # Get products that belong to the specified category and have a status of 'published'
    products = Product.objects.filter(product_status="published", category=category)
    
    context = {
        "category": category,
        "products": products,
    }
    
    return render(request, "core/category-product-list.html", context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()  # Fetch all vendors from the database
    context = {
        'vendors': vendors,
    }
    return render(request, 'core/vendor_list.html', context)


def vendor_detail_view(request, vid):
    # Fetch the vendor based on the provided vid
    vendor = get_object_or_404(Vendor, vid=vid)
    
    # Create the context dictionary
    context = {
        "vendor": vendor,
    }
    
    # Render the vendor detail template with the context
    return render(request, "core/vendor-detail.html", context)


def best_selling_products_view(request, category_id):
    # Get the specific category
    category = Category.objects.get(id=category_id)
    
    # Filter products that are best-sellers in this category
    best_selling_products = Product.objects.filter(category=category, is_best_seller=True)

    context = {
        'products': best_selling_products,
        'category': category,
    }
    return render(request, 'core/best_selling_products.html', context)

from django.shortcuts import get_object_or_404
from .models import Product, ProductReview  # Make sure to import your models
from django.db.models import Avg

def product_detail(request, pid):
    # Retrieve the product and related images
    product = get_object_or_404(Product, pid=pid)
    product_images = product.product_images.all()  # Access related ProductImages
    related_products = Product.objects.filter(category=product.category).exclude(pid=pid)[:4]
    reviews = ProductReview.objects.filter(product=product)
    average_rating = reviews.aggregate(rating=Avg('rating'))  # Aggregate the rating

    context = {
        'product': product, 
        'product_images': product_images,
        'reviews': reviews,
        'average_rating': average_rating,
        'related_products': related_products,
        'user': request.user, 
    }
    return render(request, 'core/product-detail.html', context)
