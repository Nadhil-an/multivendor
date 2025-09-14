from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from . forms import UserForm
from . models import User
from vendor.forms import VendorForm
from .models import UserProfile
from . utilis import detectUser



# Create your views here.
# -----------------------------
# User Registration
# -----------------------------

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'Already registered')
        return redirect('myaccount')
    
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.CUSTOMER       
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request,'Your Account Has Been Created ')
            return redirect('loginUser')  # reload same page
    else:
        form = UserForm()

    context = {'form': form}
    return render(request, 'accounts/userRegister.html', context)

# -----------------------------
# Vendor Registration
# -----------------------------

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered')
        return redirect('myaccount')

    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)

        if form.is_valid() and v_form.is_valid():
            # Create user
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username  = form.cleaned_data['username']
            email     = form.cleaned_data['email']
            password  = form.cleaned_data['password']

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            user.role = User.RESTAURANT
            user.save()

            # Create vendor
            vendor = v_form.save(commit=False)
            vendor.user = user

            # Safely get or create user profile
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            messages.success(request, 'Your account has been registered successfully! Please wait for approval.')
            return redirect('loginUser')   # Redirect to login instead of reloading the same page
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form
    }
    return render(request, 'accounts/RegisterVendor.html', context)

# -----------------------------
# Login
# -----------------------------

def loginUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are  already logged in')
        return redirect('myaccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            messages.success(request,'successfully login')
            return redirect('myaccount')
        else:
            messages.error(request,'Invalid login credentials')
            return redirect('loginUser')

    return render(request,'accounts/login.html')

# -----------------------------
# Logout
# -----------------------------

def logout(request):
    auth.logout(request)
    messages.info(request,'you are logged out')
    return redirect('loginUser')

# -----------------------------
# Dashboard Redirection
# -----------------------------  
@login_required(login_url='login')
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')
@login_required(login_url='login/')
def customerDashboard(request):
    return render(request, 'accounts/customerDashboard.html')


# -----------------------------
# Dashboard Views
# -----------------------------
@login_required(login_url='login')
def myaccount(request):
    if request.user.is_authenticated:
        redirecturl = detectUser(request.user)
        return redirect(redirecturl)
    else:
        return redirect('loginUser')
