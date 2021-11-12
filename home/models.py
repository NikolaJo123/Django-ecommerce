from django.contrib.auth.forms import AdminPasswordChangeForm
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.base import Model
from django.db.models.fields import DateTimeField
from django.forms import ModelForm, TextInput, Textarea
from django.utils.safestring import mark_safe
from django.http import request




# Create your models here.


class Language(models.Model):
    name= models.CharField(max_length=20)
    code= models.CharField(max_length=5)
    status=models.BooleanField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


llist = Language.objects.filter(status=True)
list1 = []
for rs in llist:
    list1.append((rs.code,rs.name))
langlist = (list1)


class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    title = models.CharField(max_length=300)
    sub_title = models.CharField(max_length=300)
    keywords = models.TextField()
    description = models.TextField()
    company = models.CharField(max_length=100)
    address = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=20)
    fax = models.CharField(blank=True, max_length=20)
    email = models.CharField(blank=True, max_length=250)
    smtpserver = models.CharField(blank=True, max_length=30)
    smtpemail = models.CharField(blank=True, max_length=50)
    smtppassword = models.CharField(blank=True, max_length=20)
    smtpport = models.CharField(blank=True, max_length=5)
    icon = models.ImageField(blank=True, upload_to='images/')
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField()
    contactus = RichTextUploadingField()
    references = RichTextUploadingField()
    customerservice = RichTextUploadingField()
    policies_and_terms = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)
    #slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class SettingLang(models.Model):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE) #many to one relation with Category
    lang =  models.CharField(max_length=6, choices=langlist)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    aboutus = RichTextUploadingField(blank=True)
    contact = RichTextUploadingField(blank=True)
    references = RichTextUploadingField(blank=True)
    
    def __str__(self):
        return self.title



class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed')
    )

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    country = models.CharField(max_length=300)
    zipcode = models.CharField(max_length=300)
    telephone = models.CharField(max_length=300)
    message = models.TextField(max_length=600)
    subject = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=50)
    note = models.CharField(blank=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'surname', 'email', 'address', 'city', 'country', 'zipcode', 'telephone', 'subject', 'message',]
        labels = {'name': '', 'surname': '', 'email':'', 'address':'', 'city':'', 'country':'', 'zipcode':'', 'telephone':'', 'subject':'', 'message':''}
        widgets = {
            'name' : TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}),
            'surname' : TextInput(attrs={'class': 'input', 'placeholder': 'last Name'}),
            'email' : TextInput(attrs={'class': 'input', 'placeholder': 'Email Address'}),
            'address' : TextInput(attrs={'class': 'input', 'placeholder': 'Address'}),
            'city' : TextInput(attrs={'class': 'input', 'placeholder': 'City'}),
            'country' : TextInput(attrs={'class': 'input', 'placeholder': 'Country'}),
            'zipcode' : TextInput(attrs={'class': 'input', 'placeholder': 'ZIP/Postal COde'}),
            'telephone' : TextInput(attrs={'class': 'input', 'placeholder': 'Telephone'}),
            'subject' : TextInput(attrs={'class': 'input', 'placeholder': 'Subject'}),
            'message' : Textarea(attrs={'class': 'input', 'placeholder': 'Your Message', 'rows': '5'}),
        }


class AlertCat(models.Model):
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class MessageAlert(models.Model):
    category = models.ForeignKey(AlertCat, blank=True, on_delete=models.CASCADE)
    name = models.CharField(blank=True, max_length=200)
    message = models.CharField(blank=True, max_length=300)

    def __str__(self):
        #if category == AlertCat.value('')
        return self.message


class FAQ(models.Model):
    STATUS = (
        ("True", True),
        ("False", False),
    )

    lang = models.CharField(max_length=6, choices=langlist, null=True)
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=500)
    answer = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question