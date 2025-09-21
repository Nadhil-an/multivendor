from django.urls import path
from . import views

urlpatterns = [
    path('registerUser/',views.registerUser,name='registerUser'),
    path('registerVendor/',views.registerVendor,name='registerVendor'),
    path('login/', views.loginUser, name='loginUser'),
    path('logout/', views.logout, name='logout'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('vendorDashboard/', views.vendorDashboard, name='vendorDashboard'),
    path('customerDashboard/', views.customerDashboard, name='customerDashboard'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    
    path('resetpassword/<uidb64>/<token>/',views.resetpassword,name='resetpassword'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
]
