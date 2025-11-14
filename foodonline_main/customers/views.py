from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm,UserInfoForm
# Create your views here.
@login_required(login_url='login')
def cprofile(request):
    userprofile_form = UserProfileForm()
    user_form = UserInfoForm()

    context ={
        'user_form':user_form,
        'userprofile_form':userprofile_form,
        
    }

    return render(request,'customer/cprofile.html',context)