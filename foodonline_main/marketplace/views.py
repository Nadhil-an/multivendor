from django.shortcuts import render,get_object_or_404
from vendor.models import Vendor
from menu.models import Category,FoodItem
from marketplace.models import Cart
from django.http import HttpResponse,JsonResponse

from django.db.models import Prefetch

# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True,user__is_active=True)
    count = vendors.count()
    context={
        'vendors':vendors,
        'count':count
    }
    return render(request,'marketplace/listing.html',context)


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

def add_to_cart(request,food_id=None):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            try:
                fooditem = FoodItem.objects.get(id=food_id)
            except FoodItem.DoesNotExist:
                return JsonResponse({'status':'failed','message':'This food does not exist'})

            try:
                chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                chkCart.quantity += 1
                chkCart.save()
                return JsonResponse({'status':'Success','message':'Increased the cart quantity'})
            except Cart.DoesNotExist:
                Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                return JsonResponse({'status':'Success','message':'Product added to the cart'})

        return JsonResponse({'status':'failed','message':'Invalid Request'})

    else:
        return JsonResponse({'status':'failed','message':'Please login to continue'})
    