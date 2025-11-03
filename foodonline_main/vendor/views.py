from django.shortcuts import render,get_object_or_404,redirect
from . models import Vendor,OpeningHour
from django.http import HttpResponse
from .forms import VendorForm,OpeningHourForm
from accounts.models import UserProfile
from accounts.forms import UserProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from django.conf import settings
from menu.models import Category,FoodItem
from menu.forms import CategoryForm,FoodItemForm
from django.template.defaultfilters import slugify  
from django.views.decorators.cache import never_cache



##################################
#
# Create Vendor Profile
#
###################################

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
        'GOOGLE_API_KEY': settings.GOOGLE_API_KEY,
        
    }
    
    return render(request,'vendor/vprofile.html',context)

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


##################################
#
# Menu Builder
#
###################################

@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    category = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'category':category
    }
    return render(request,'vendor/menu_builder.html',context)



##################################
#
# Food_items by category
#
###################################
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

##################################
#
# Add Category
#
###################################

@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.save()

            category.slug = slugify(category_name)+'-'+str(category.id) # ✅ assign vendor
            category.save()
              # ✅ slug auto-handled in model.save()
            messages.success(request, 'Category added Successfully')
            return redirect('menu_builder')
    else:
        form = CategoryForm()

    # ✅ context is always defined
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)


##################################
#
# Edit Category
#
###################################

@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def edit_category(request,pk=None):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST,instance=category)
    if form.is_valid():
            category = form.save(commit=False)
            category.vendor = get_vendor(request)  # ✅ assign vendor
            category.save()  # ✅ slug auto-handled in model.save()
            messages.success(request, 'Category updated Successfully')
            return redirect('menu_builder')
    else:
        form = CategoryForm(instance=category)

    # ✅ context is always defined
    context = {
        'form': form,
        'category':category,
    }
    return render(request,'vendor/edit_category.html',context)

##################################
#
# Delete Category
#
###################################

@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def delete_category(request,pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()

    messages.success(request,'Category Successfully delete')
    return redirect('menu_builder') 


##################################
#
# Add Food Item
#
###################################


@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)    
def addfood(request):

    if request.method == 'POST':
        form = FoodItemForm(request.POST,request.FILES)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug= slugify(food_title) 
            food.save() 
            messages.success(request, 'Food Successfully Added')
            return redirect('fooditems_by_category',food.category.id)
    else:
        form = FoodItemForm()
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

    context = {
        'form':form
        
    }
    return render(request,'vendor/addfood.html',context)


##################################
#
# Edit food item
#
###################################
@login_required(login_url='loginUser')
@user_passes_test(check_role_vendor)
def edit_food(request,pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == "POST":
        form = FoodItemForm(request.POST,request.FILES,instance=food )
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
        if form.is_valid():
                food = form.save(commit=False)
                food.vendor = get_vendor(request)  # ✅ assign vendor
                food.save()  # ✅ slug auto-handled in model.save()
                messages.success(request, 'FoodItem updated Successfully')
                return redirect('fooditems_by_category', food.category.id)
        else:
            print(form.errors)

    else:
        form = FoodItemForm(instance=food)  
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

    # ✅ context is always defined
    context = {
        'form': form,
        'food':food,
    }
    return render(request,'vendor/edit_food.html',context)
##################################
#
# Edit food item
#
###################################
@login_required(login_url='loginUser')
def delete_food(request,pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()

    messages.success(request,'Food item delete successfully ')
    return redirect('menu_builder') 


##################################
#
# Opening Hours
#
###################################
def opening_hours(request):
    opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request))
    form = OpeningHourForm() 
    context = {
        'form':form,
        'opening_hours':opening_hours,
    }
    return render(request,'vendor/opening_hours.html',context)

def add_hour(request):
    return HttpResponse('add_hour')


