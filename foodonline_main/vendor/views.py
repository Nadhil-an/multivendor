from django.shortcuts import render,get_object_or_404,redirect
from . models import Vendor
from . forms import VendorForm
from accounts.models import UserProfile
from accounts.forms import UserProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from django.conf import settings
from menu.models import Category




# Create your views here.
@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def vprofile(request):
    
    profile = get_object_or_404(UserProfile, user = request.user)
    vendor_get = get_object_or_404(Vendor, user = request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor_get)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Settings Updated.')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor_get)

    
    context = {
        'profile':profile,
        'vendor_get':vendor_get,
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        "MAPBOX_PUBLIC_TOKEN": settings.MAPBOX_PUBLIC_TOKEN
    }
    
    return render(request,'vendor/vprofile.html',context)

def menu_builder(request):
    vendor = Vendor.objects.get(user=request.user)
    category = Category.objects.filter(vendor=vendor)
    context = {
        'category':category
    }
    return render(request,'vendor/menu_builder.html',context)
