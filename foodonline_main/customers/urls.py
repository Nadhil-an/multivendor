from django.urls import path,include
from accounts import views as AccountViews
from . import views

urlpatterns = [
    path('', AccountViews.customerDashboard, name='customerDashboard'),
    path('profile/',views.cprofile,name='cprofile'),
    path('my_order/',views.my_order,name='my_order'),
    path('order_details/<int:order_number>/', views.order_details, name='order_details'),
    


]