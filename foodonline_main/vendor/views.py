from django.shortcuts import render,get_object_or_404,redirect
from . models import Vendor
from . forms import VendorForm
from accounts.models import UserProfile
from accounts.forms import UserProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from django.conf import settings
from menu.models import Category,FoodItem
from menu.forms import CategoryForm
from django.template.defaultfilters import slugify  




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

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    category = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'category':category
    }
    return render(request,'vendor/menu_builder.html',context)

@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request,pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category,pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)

    context = {
        'category':category,
        'fooditems':fooditems
    }
    return render(request,'vendor/menu_category.html',context)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.vendor = get_vendor(request)  # ✅ assign vendor
            category.save()  # ✅ slug auto-handled in model.save()
            messages.success(request, 'Category added Successfully')
            return redirect('menu_builder')
    else:
        form = CategoryForm()

    # ✅ context is always defined
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)

def edit_category(request,pk=None):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST,instance=category)
    if form.is_valid():
            category = form.save(commit=False)
            category.vendor = get_vendor(request)  # ✅ assign vendor
            category.save()  # ✅ slug auto-handled in model.save()
            messages.success(request, 'Category uodated Successfully')
            return redirect('menu_builder')
    else:
        form = CategoryForm(instance=category)

    # ✅ context is always defined
    context = {
        'form': form,
        'category':category,
    }
    return render(request,'vendor/edit_category.html',context)
