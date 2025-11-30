from django.urls import path,include
from accounts import views as AccountViews
from . import views

urlpatterns = [
    path('', AccountViews.customerDashboard, name='customerDashboard'),
    path('profile/',views.cprofile,name='cprofile'),
    path('order_details/',views.order_details,name='order_details'),

]