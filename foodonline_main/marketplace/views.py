from django.shortcuts import render,get_object_or_404
from vendor.models import Vendor
from menu.models import Category,FoodItem
from .models import Cart
from . context_processor import get_cart_counter
from django.http import JsonResponse,HttpResponse

from django.db.models import Prefetch
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
    vendor = get_object_or_404(Vendor,vendor_slug=vendor_slug)
    category = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        )
    )
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context={
        'vendor':vendor,
        'category':category,
        'cart_items':cart_items,
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
                return JsonResponse({'status':'Success','message':'Increased the cart quantity','cart_counter':get_cart_counter(request), 'qty':chkCart.quantity})
            except Cart.DoesNotExist:
                newCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                return JsonResponse({'status':'Success','message':'Product added to the cart','cart_counter':get_cart_counter(request), 'qty':newCart.quantity})

        return JsonResponse({'status':'failed','message':'Invalid Request'})

    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
#######################
#
# decrease_cart
#
#######################
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
                return JsonResponse({'status':'Success','message':'Remove the cart quantity','cart_counter':get_cart_counter(request), 'qty':qty})
            except Cart.DoesNotExist:
               
                return JsonResponse({'status':'failed','message':'You do not have item in your cart', 'qty':0})

        return JsonResponse({'status':'failed','message':'Invalid Request'})

    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
    
def cart(request):
    cart = Cart.objects.filter(user=request.user)
    context = {
        'cart_items':cart,
    }
    return render(request,'marketplace/cart.html',context)


    