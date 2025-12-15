from django.shortcuts import render,get_object_or_404,redirect
from vendor.models import Vendor
from menu.models import Category,FoodItem
from .models import Cart
from vendor.models import OpeningHour
from accounts.models import UserProfile
from orders.forms import OrderForm
from . context_processor import get_cart_counter,get_cart_amount
from django.http import JsonResponse,HttpResponse
from django.db.models import Q
from django.db.models import Prefetch
from datetime import date,datetime
from django.contrib.auth.decorators import login_required


from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
#######################
#
# market place
# 
#######################
# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True,user__is_active=True)
    count = vendors.count()
    context={
        'vendors':vendors,
        'count':count
    }
    return render(request,'marketplace/listing.html',context)
#######################
# vendor_details
#######################

def parse_time_string(value):
    """Convert '09:00' or '09:00 AM' into datetime.time object."""
    if isinstance(value, str):
        for fmt in ("%H:%M", "%I:%M %p"):
            try:
                return datetime.strptime(value, fmt).time()
            except ValueError:
                continue
    return None


def vendor_details(request, vendor_slug, category_slug=None):
    today_date = date.today()
    today = today_date.isoweekday()

    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)

    # --- Opening Hours ---
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', '-from_hour')
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor, day=today)

    # Check if vendor is open NOW
    # Check if vendor is open NOW
    is_open = False
    now = datetime.now().time()

    for i in current_opening_hours:

        if not i.from_hour or not i.to_hour:
            continue

        if i.is_closed:
            continue

        start = parse_time_string(i.from_hour)
        end = parse_time_string(i.to_hour)

        if not start or not end:
            continue

        if start <= now <= end:
            is_open = True



    # --- Category List ---
    categories = Category.objects.filter(vendor=vendor)

    # --- If Category Selected ---
    if category_slug:
        selected_category = get_object_or_404(Category, vendor=vendor, slug=category_slug)
        foods = FoodItem.objects.filter(category=selected_category, is_available=True).order_by('food_title')

    else:
        selected_category = None
        foods = FoodItem.objects.filter(vendor=vendor, is_available=True).order_by('category__category_name', 'food_title')

    # Category with foods mapping (for full view)
    category_with_food = {}
    for cat in categories:
        category_with_food[cat] = FoodItem.objects.filter(category=cat, is_available=True)

    # --- User Cart ---
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_items_dict = {item.fooditem.id: item.quantity for item in cart_items}
    else:
        cart_items = None
        cart_items_dict = {}

    context = {
        'vendor': vendor,

        # categories in sidebar
        'categories': categories,

        # foods returned based on slug
        'foods': foods,

        # mapping for full list view
        'category_with_food': category_with_food,

        # highlight sidebar selected item
        'selected_category': selected_category,

        # cart details
        'cart_items': cart_items,
        'cart_items_dict': cart_items_dict,

        # opening hour data
        'opening_hours': opening_hours,
        'current_opening_hours': current_opening_hours,
        'is_open': is_open,
    }

    return render(request, 'marketplace/vendor_details.html', context)

#######################
#
# add_to_cart
#
####################### 
def add_to_cart(request, food_id):

    if  request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    chkCart.quantity +=1
                    chkCart.save()
                    return JsonResponse({'status':'Success','message':'Increase the cart quantity','cart_counter':get_cart_counter(request),'qty':chkCart.quantity})
                except:
                    chkCart = Cart.objects.create(user=request.user,fooditem=fooditem,quantity=1)
                    return JsonResponse({'status':'Success','message':'Added to food to the cart','cart_counter':get_cart_counter(request),'qty':chkCart.quantity})
            except:
                return JsonResponse({'status':'Failed','message':'This food does not exist!'})
            
    
    else:
        return JsonResponse({'status':'Failed','message':'Invalid Request'})
        

    


    
    

########################
#
# decrease_cart
#
########################
def decrease_cart(request,food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            try:
                #check if the food item is available
                fooditem = FoodItem.objects.get(id=food_id)
            except FoodItem.DoesNotExist:
                return JsonResponse({'status':'failed','message':'This food does not exist'})

            try:
                #checking if the food item is already added to the cart
                chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                if chkCart.quantity >1:
                    chkCart.quantity -= 1
                    chkCart.save()
                    qty = chkCart.quantity
                else:
                    chkCart.delete()
                    qty=0
                return JsonResponse({'status':'Success','message':'Remove the cart quantity','cart_counter':get_cart_counter(request), 'qty':qty,'cart_amount':get_cart_amount(request)})
            except Cart.DoesNotExist:
               
                return JsonResponse({'status':'failed','message':'You do not have item in your cart', 'qty':0,'cart_amount':get_cart_amount(request)})

        return JsonResponse({'status':'failed','message':'Invalid Request'})

    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
    
def cart(request):
    cart = Cart.objects.filter(user=request.user)
    context = {
        'cart_items':cart,
    }
    return render(request,'marketplace/cart.html',context)


def delete_item(request, food_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})

    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'status':'failed','message':'Invalid Request'})

    try:
        # Get the cart item for this user and food item
        cart_item = Cart.objects.get(user=request.user, fooditem_id=food_id)
        cart_item.delete()
        return JsonResponse({
            'status':'Success',
            'message':'Cart Item has been deleted!',
            'cart_counter': get_cart_counter(request), 
             'cart_amount':get_cart_amount(request) # returns updated cart count
        })
    except Cart.DoesNotExist:
        return JsonResponse({'status':'failed','message':'Cart Item does not exist'})


def search(request):
    if 'address' not in request.GET:
        return redirect('marketplace')

    address = request.GET.get('address')
    longitude = request.GET.get('lng')
    latitude = request.GET.get('lat')
    radius = request.GET.get('radius')
    keyword = request.GET.get('rest_name')

    # Step 1: Base vendor query
    vendors = Vendor.objects.filter(
        Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True)
    )

    # Step 2: Match vendors by food items
    fetch_vendor_by_fooditems = FoodItem.objects.filter(
        food_title__icontains=keyword, is_available=True
    ).values_list('vendor', flat=True)

    vendors = Vendor.objects.filter(
        Q(id__in=fetch_vendor_by_fooditems) |
        Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True)
    )

    # Step 3: If coordinates provided, calculate distance
    if latitude and longitude and radius:
        try:
            lat = float(latitude)
            lng = float(longitude)
            rad = float(radius)
        except ValueError:
            lat = lng = rad = None

        if lat and lng and rad:
            pnt = GEOSGeometry(f'POINT({lng} {lat})', srid=4326)
            vendors = vendors.filter(
                user_profile__location__distance_lte=(pnt, D(km=rad))
            ).annotate(
                distance=Distance("user_profile__location", pnt)
            ).order_by("distance")

            # ✅ Assign readable distance in km
            for v in vendors:
                v.km = round(v.distance.km, 2)

    # Step 4: Count vendors
    vendor_count = vendors.count()

    # Step 5: Render template
    context = {
        'vendors': vendors,
        'count': vendor_count,
        'source_location': address,
    }

    return render(request, 'marketplace/listing.html', context)


@login_required(login_url='login')
def checkout(request):
    # Fetch the user's cart items
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()

    # If cart is empty, redirect user
    if cart_count == 0:
        return redirect('marketplace')

    # Get user profile safely
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Default values for pre-filled form
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code,
    }

    # Pre-filled order form
    form = OrderForm(initial=default_values)

    # Context
    context = {
        'form': form,
        'cart_items': cart_items,
    }

    return render(request, 'marketplace/checkout.html', context)