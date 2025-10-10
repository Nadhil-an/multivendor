from django.shortcuts import render,get_object_or_404
from vendor.models import Vendor
from menu.models import Category

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
    category = Category.objects.filter(vendor=vendor)

    context={
        'vendor':vendor,
        'category':category,
    }

   
    return render(request,'marketplace/vendor_details.html',context)
