from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models.aggregates import Avg, Count
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.forms import ModelForm, TextInput, Textarea
from home.models import Language





# Create your models here.
class Categorie(MPTTModel):
    STATUS = (
        ('True', 'Yes'),
        ('False', 'No')
    )

    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class MPTTMeta:
        order_insertion_by = ['title']

    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})
        #return reverse('category_detail', kwargs=[str(self.slug)])
    

    def __str__(self):                  # __str__ method elaborated later in
        full_path = [self.title]        # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])
    


class Product(models.Model):
    STATUS = (
        ('True', 'Yes'),
        ('False', 'No')
    )

    VARIANTS = (
        ('None','None'),
        ('Size','Size'),
        ('Color','Color'),
        ('Size-Color','Size-Color'),
    )

    category = models.ForeignKey(Categorie, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    keywords = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(blank=True, upload_to='images/')
    price = models.FloatField()
    amount = models.IntegerField()
    #detail = models.TextField()
    detail = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)
    variant=models.CharField(max_length=10,choices=VARIANTS, default='None')
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})
        #return reverse('category_detail', kwargs=[str(self.slug)])
    
    def averagereview(self):
        reviews = ReviewMessage.objects.filter(product=self, status='Read').aggregate(average=Avg('rate'))
        avg = 0
        
        if reviews["average"] is not None:
            avg = float(reviews['average'])
        return avg
    

    def countreview(self):
        reviews = ReviewMessage.objects.filter(product=self).aggregate(average=Count('id'))
        cnt = 0
        
        if reviews["count"] is not None:
            cnt = int(reviews['count'])
        return cnt
    

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""
    

    '''def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50" width="50"/>'.format(self.image.url))
        else:
            return ""
    '''
    

    '''def image_tag(self):
        return mark_safe('<img src="{}" heignt="50" width="50"/>'.format(self.image.url))'''

    image_tag.short_description = "Image"
    image_tag.allow_tags = True
    

class Images(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title


class ReviewMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed')
    )
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=300)
    subject = models.CharField(max_length=100, blank=True)
    comment = models.TextField(max_length=600)
    ip = models.TextField(max_length=20, blank=True)
    rate = models.IntegerField(default=1)
    status = models.CharField(max_length=50, choices=STATUS, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Comment_ReviewForm(ModelForm):
    class Meta:
        model = ReviewMessage
        fields = ['name', 'subject', 'email', 'comment', 'rate']
        labels = {'name': '', 'subject': '', 'email':'', 'comment':''}
        widgets = {
            'name' : TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}),
            'subject' : TextInput(attrs={'class': 'input', 'placeholder': 'subject'}),
            'email' : TextInput(attrs={'class': 'input', 'placeholder': 'Email Address'}),
            'comment' : Textarea(attrs={'class': 'input', 'placeholder': 'Your Review'}),
        }
    

class Setting(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    title = models.CharField(max_length =50, blank=True)
    caption = models.CharField(max_length =50, blank=True)
    second_caption = models.CharField(max_length =50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        #cap = (self.caption, self.second_caption)
        return self.caption


class Color(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, blank=True,null=True)
    
    def __str__(self):
        return self.name
    
    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, blank=True,null=True)
    
    def __str__(self):
        return self.name


class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    image_id = models.IntegerField(blank=True,null=True,default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)

    
    def __str__(self):
        return self.title
    

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image.url
        else:
            varimage=""
        return varimage
    

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
           return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""


llist= Language.objects.all()
list1=[]
for rs in llist:
    list1.append((rs.code,rs.name))
langlist= (list1)


class ProductLang(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #many to one relation with Category
    lang =  models.CharField(max_length=6, choices=langlist)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(null=False, unique=True)
    detail=RichTextUploadingField()

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class CategoryLang(models.Model):
    category = models.ForeignKey(Categorie, related_name='categorylangs', on_delete=models.CASCADE) #many to one relation with Category
    lang =  models.CharField(max_length=6, choices=langlist)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    slug = models.SlugField(null=False, unique=True)
    description = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


