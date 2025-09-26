from django.shortcuts import render,get_object_or_404
from . models import Vendor
from . forms import VendorForm
from accounts.models import UserProfile
from accounts.forms import UserProfileForm

# Create your views here.

def vprofile(request):
    
    profile = get_object_or_404(UserProfile, user = request.user)
    vendor_get = get_object_or_404(Vendor, user = request.user)

    profile_form = UserProfileForm(instance=profile)
    vendor_form = VendorForm(instance=vendor_get)
    context = {
        'profile':profile,
        'vendor_get':vendor_get,
        'profile_form':profile_form,
        'vendor_form':vendor_form
    }


    
    return render(request,'vendor/vprofile.html',context)
