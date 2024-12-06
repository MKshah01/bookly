from django.http import HttpResponse , JsonResponse
from django.core.exceptions import ObjectDoesNotExist
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


def product_detail(request, pid):
    # Retrieve the product and related images
    product = get_object_or_404(Product, pid=pid)
    product_images = product.product_images.all()  # Access related ProductImages
    related_products = Product.objects.filter(category=product.category).exclude(pid=pid)[:4]
    reviews = ProductReview.objects.filter(product=product)
    average_rating = reviews.aggregate(rating=Avg('rating'))  # Aggregate the rating
    reviews_form = ProductReviewForm()

    context = {
        'product': product, 
        'product_images': product_images,
        'reviews': reviews,
        'average_rating': average_rating,
        'related_products': related_products,
        'reviews_form': reviews_form,
        'user': request.user, 
    }
    return render(request, 'core/product-detail.html', context)


def ajax_add_review(request, pid):
    try:
        # Retrieve product and user
        product = Product.objects.get(pid=pid)
        user = request.user
        
        # Create the review
        review = ProductReview.objects.create(
            user=user,
            product=product,
            review=request.POST['review'],
            rating=request.POST['rating'],
        )

        # Prepare the context with user info and review details
        context = {
            "user": user.username,
            "review": request.POST['review'],
            "rating": request.POST['rating'],
        }

        # Calculate the average rating for the product
        average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
        
        return JsonResponse({
            "bool": True,
            "context": context,
            "average_reviews": average_reviews['rating'],
        })

    except ObjectDoesNotExist:
        return JsonResponse({"bool": False, "error": "Product not found."}, status=404)
    except Exception as e:
        print("Error:", e)  # Log the error for debugging
        return JsonResponse({"bool": False, "error": str(e)}, status=500)

def search_view(request):
    # Get the search query from the GET request
    query = request.GET.get('q', '')  # Default to an empty string if 'q' is not provided

    # Filter products based on the search query in title or description
    products = Product.objects.filter(title__icontains=query).order_by("-date")
    # Set up the context with the search results and query
    context = {
        "products": products,
        "query": query,
    }

    # Render the search.html template with the context data
    return render(request, "core/search.html", context)


def add_to_cart_ajax(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'You need to log in to add items to the cart.'}, status=401)

    try:
        user = request.user
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)

        # Create or retrieve a cart order for the user
        cart_order, created = CartOrder.objects.get_or_create(
            user=user,
            paid_status=False  # Only get the current active cart
        )

        # Add or update the item in cart order items
        cart_item, item_created = CartOrderItems.objects.get_or_create(
            order=cart_order,
            item=product.title,
            defaults={
                'invoice_no': generate_invoice_number(),  # Replace with your dynamic invoice generation logic
                'product_status': 'Pending',
                'qty': quantity,
                'price': product.price,
                'total': product.price * quantity,
                'image': product.image.url  # Ensure image field exists or adjust accordingly
            }
        )

        if not item_created:
            # Update quantity and total if the item already exists in the cart
            cart_item.qty += quantity
            cart_item.total = cart_item.qty * cart_item.price
            cart_item.save()

        # Return JSON response with updated cart count
        return JsonResponse({
            'success': True,
            'cart_count': CartOrderItems.objects.filter(order=cart_order).count()
        })

    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

def generate_invoice_number():
    import uuid
    return f"INV-{uuid.uuid4().hex[:8].upper()}"


def add_to_cart(request):
    cart_product = {
        str(request.GET['id']): {
            'title': request.GET['title'],
            'qty': int(request.GET['qty']),
            'price': float(request.GET["price"])
        }
    }
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] += int(request.GET['qty'])
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    # Return the updated cart data and total number of items in the cart
    return JsonResponse({
        "data": request.session['cart_data_obj'], 
        "totalcartitems": len(request.session['cart_data_obj'])
    })
