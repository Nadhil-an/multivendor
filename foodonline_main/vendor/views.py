from django.shortcuts import render
from . models import Vendor


# Create your views here.

def vprofile(request):
    vendor = Vendor.objects.get(user=request.user)
    context = {
        'vendor':vendor
    }
    return render(request,'vendor/vprofile.html',context)
