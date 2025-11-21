from django.contrib import admin
from . models import Payment,Order,OrderedFood


class OrderFoodInline(admin.TabularInline):
    models = OrderedFood
    readonly_fields = ('order','payment','user','fooditem','quantity','price','amount')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','name','phone','email','total','payment_method','status','is_ordered']
    inlines = [OrderFoodInline]
# Register your models here.
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderedFood)
