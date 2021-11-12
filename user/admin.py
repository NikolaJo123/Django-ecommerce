from django.contrib import admin
from user.models import UserProfile, UserFavourites





# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'address', 'phone', 'city', 'country', 'image_tag',]
    list_filter = ['address', 'phone', 'city', 'country',]
    #prepopulated_fields = {'title': ('subject',)}


class UserFavouritesAdmin(admin.ModelAdmin):
    list_display = ['user', 'product_name', 'price', 'date_added', 'image']
    list_filter = ['user', 'product_name']
    readonly_fields = ('variant', 'user', 'product_name', 'price', 'quantity')



admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserFavourites, UserFavouritesAdmin)

