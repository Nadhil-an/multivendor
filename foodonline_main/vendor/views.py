from django.shortcuts import render,get_object_or_404,redirect
from . models import Vendor
from . forms import VendorForm
from accounts.models import UserProfile
from accounts.forms import UserProfileForm
from django.contrib import messages

# Create your views here.

def vprofile(request):
    
    profile = get_object_or_404(UserProfile, user = request.user)
    vendor_get = get_object_or_404(Vendor, user = request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor_get)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.form.save()
            vendor_form.save()
            messages.success(request,'Settings Updated.')
            return redirect('vprofile')
        else:
            print(profile_form.error)
            print(vendor_form.error)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor_get)

    
    context = {
        'profile':profile,
        'vendor_get':vendor_get,
        'profile_form':profile_form,
        'vendor_form':vendor_form
    }


    
    return render(request,'vendor/vprofile.html',context)
