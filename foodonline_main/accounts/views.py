from django.shortcuts import render,redirect
from . forms import UserForm
from . models import User

# Create your views here.


def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.CUSTOMER       
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('registerUser')  # reload same page
    else:
        form = UserForm()

    context = {'form': form}
    return render(request, 'accounts/userRegister.html', context)
