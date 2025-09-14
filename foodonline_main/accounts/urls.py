from django.urls import path
from . import views

urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('login/', views.loginUser, name='loginUser'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    
]
