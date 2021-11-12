from django.db import models
from django.db.models.base import Model
from django.db.models.fields.files import ImageField
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.urls import reverse
from home.models import Language
from currencies.models import Currency
from product.models import Product, Variants
from django.forms import ModelForm





# Create your models here.
class UserProfile(models.Model):
    STATUS = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Blocked', 'Blocked')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=200)
    city = models.CharField(blank=True, max_length=50)
    country = models.CharField(blank=True, max_length=50)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='Inactive')
    image = models.ImageField(blank=True, upload_to='images/users/')


    def __str__(self):
        return self.user.username


    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'slug': self.slug})
    
    
    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + ']'
    

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    
    '''def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))'''
    
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class UserFavourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product_name = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def price(self):
        return (self.product_name.price)
    
    @property
    def image(self):
        return (self.product_name.image_tag)


class UserFavouritesForm(ModelForm):
    class Meta:
        model = UserFavourites
        fields = ['quantity']
