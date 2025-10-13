from django.urls import path
from . import views

urlpatterns = [
    path('',views.marketplace,name='marketplace'),
    path('<slug:vendor_slug>/', views.vendor_details,name='vendor_details'),


    #Add_to_cart
    path('add_to_cart/<int:food_id>/',views.add_to_cart,name='add_to_cart'),
    #Decrease Cart
    path('decrease_cart/<int:food_id>/',views.decrease_cart,name='decrease_cart'),
    #Delete cart item
    path('delete/<int:food_id>/',views.delete_item,name='delete_item'),
   
]