from django.shortcuts import render,get_object_or_404,redirect
from vendor.models import Vendor
from menu.models import Category,FoodItem
from .models import Cart
from vendor.models import OpeningHour
from . context_processor import get_cart_counter,get_cart_amount
from django.http import JsonResponse,HttpResponse
from django.db.models import Q
from django.db.models import Prefetch
from datetime import date,datetime

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
#
# vendor_details
#
#######################
def vendor_details(request,vendor_slug):
     # getting current day
    today_date =date.today()
    today = today_date.isoweekday()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    is_open = None
    vendor = get_object_or_404(Vendor,vendor_slug=vendor_slug)
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day','-from_hour')
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor,day=today)



    for i in current_opening_hours:
        # Convert to time object safely (handles both TimeField and string)
        if isinstance(i.from_hour, str):
            try:
                start_time = datetime.strptime(i.from_hour, "%I:%M:%p").time()
            except ValueError:
                start_time = datetime.strptime(i.from_hour, "%H:%M:%S").time()
        else:
            start_time = i.from_hour

        if isinstance(i.to_hour, str):
            try:
                end_time = datetime.strptime(i.to_hour, "%I:%M:%p").time()
            except ValueError:
                end_time = datetime.strptime(i.to_hour, "%H:%M:%S").time()
        else:
            end_time = i.to_hour

        now = datetime.now().time()

        if start_time <= now <= end_time and not i.is_closed:
            is_open = True
            break
        else:
            is_open = False


    current_opening_hours = OpeningHour.objects.filter(vendor=vendor,day=today)
    category = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        )
    )
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        cart_items_dict = {item.fooditem.id: item.quantity for item in cart_items}
    else:
        cart_items = None
        cart_items_dict = {}
    context={
        'vendor':vendor,
        'category':category,
        'cart_items':cart_items,
        'cart_items_dict': cart_items_dict,
        'opening_hours':opening_hours,
        'current_opening_hours':current_opening_hours,
        'is_open':is_open,
    }
    return render(request,'marketplace/vendor_details.html',context)
#######################
#
# add_to_cart
#
#######################
def add_to_cart(request,food_id=None):
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
                chkCart.quantity += 1
                chkCart.save()
                return JsonResponse({'status':'Success','message':'Increased the cart quantity','cart_counter':get_cart_counter(request), 'qty':chkCart.quantity,'cart_amount':get_cart_amount(request)})
            except Cart.DoesNotExist:
                newCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                return JsonResponse({'status':'Success','message':'Product added to the cart','cart_counter':get_cart_counter(request), 'qty':newCart.quantity,'cart_amount':get_cart_amount(request)})

        return JsonResponse({'status':'failed','message':'Invalid Request'})

    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
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
