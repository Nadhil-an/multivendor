from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm,UserInfoForm
from accounts.models import UserProfile,User
# Create your views here.
@login_required(login_url='login')
def cprofile(request):
    profile = get_object_or_404(UserProfile,user=request.user)

    userprofile_form = UserProfileForm(instance=profile)
    user_form = UserInfoForm(instance=request.user)

    context ={
        'user_form':user_form,
        'userprofile_form':userprofile_form,
        
    }

    return render(request,'customer/cprofile.html',context)