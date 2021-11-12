from functools import total_ordering

from django.http.response import JsonResponse
from django.utils import translation
from product.admin import Comment_Review
from django import forms
from django.db.models import query
from django.db.models.functions import Concat
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from home.models import Setting, ContactForm, ContactMessage, MessageAlert, FAQ, SettingLang, Language
from product.models import Categorie, Images, Product, ReviewMessage, Comment_ReviewForm, Variants, Color, Size, ProductLang, CategoryLang
from product.models import Setting as PS
from django.contrib import messages
from home.forms import SearchForm
from order.models import ShopCart
from ecommerce import settings
from user.models import UserProfile
from currencies.models import Currency
import json
#from django.utils.translation import gettext as _



# Create your views here.
def error_404_view(request, ex):
    return render(request,'404.html')
    #return HttpResponse('Error Page 404')



def index(request):
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    category = Categorie.objects.all()
    products_slider = Product.objects.all().order_by('id')[:4]
    latest_products_slider = Product.objects.all().order_by('-id')[:4]
    #deals_products_slider = Product.objects.all().order_by('-id')[:3]
    random_picked_products_slider = Product.objects.all().order_by('?')[:3] # Random selected 4 products
    page = 'home'
    empt_list = True
    total_products = 0
    total = 0

    # Currency start.
    defaultcurr = settings.DEFAULT_CURRENCY
    
    if not request.session.has_key('currency'):
        request.session['currency'] = settings.DEFAULT_CURRENCY
    # Currency end.

    for rs in shopcart:
        total += rs.price * rs.quantity

    for rs in shopcart:
        total_products += rs.quantity
    
    # >>>>>>>>>>>>>>>> M U L T I   L A N G U G A E >>>>>> START
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]

    if defaultlang != currentlang:
        setting = SettingLang.objects.get(lang=currentlang)
        latest_products_slider = Product.objects.raw(
            'SELECT p.id,p.price, l.title, l.description,l.slug  '
            'FROM product_product as p '
            'LEFT JOIN product_productlang as l '
            'ON p.id = l.product_id '
            'WHERE  l.lang=%s ORDER BY p.id DESC LIMIT 4', [currentlang])

    #caption = PS.objects.all().order_by('-id')[:3]


    context = {'setting':setting, 
                'page': page,
                'empty': empt_list, 
                'category': category,
                'products_slider': products_slider,
                'latest_products_slider': latest_products_slider,
                'random_picked_products_slider': random_picked_products_slider,
                'shopcart': shopcart,
                'total_products': total_products,
                'total': total,
                }
    return render(request, 'index.html', context)

    #university = 'Karabuk University'
    #dept = 'Computer Engineering'
    #context = {'university':university, 'department':dept}
    #return render(request, 'index.html', context)
    #return HttpResponse('Hello World')


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    category = Categorie.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_products = 0
    total = 0
    
    for rs in shopcart:
        total += rs.price * rs.quantity

    for rs in shopcart:
        total_products += rs.quantity
    
    if defaultlang != currentlang:
        setting = SettingLang.objects.get(lang=currentlang)

    context = {'setting':setting, 'category': category, 'shopcart': shopcart, 'total_products': total_products, 'total': total,}
    return render(request, 'aboutus.html', context)

    #return HttpResponse('About Us')


def contactus(request):
    message = MessageAlert.objects.get()
    currentlang = request.LANGUAGE_CODE[0:2]
    if request.method == 'POST':
        form = ContactForm(request.POST) # Check post.
        if form.is_valid():
            data = ContactMessage() # Create relation with model.
            data.name = form.cleaned_data['name'] # Get form input data.
            data.surname = form.cleaned_data['surname']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            data.zipcode = form.cleaned_data['zipcode']
            data.telephone = form.cleaned_data['telephone']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save() # Save data to table
            messages.success(request, message)
            return HttpResponseRedirect('/contactus')
        
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    setting = Setting.objects.get(pk=1)
    
    if defaultlang != currentlang:
        setting = SettingLang.objects.get(lang=currentlang)

    form = ContactForm
    category = Categorie.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_products = 0
    total = 0
    
    for rs in shopcart:
        total += rs.price * rs.quantity

    for rs in shopcart:
        total_products += rs.quantity

    context = {'setting':setting, 'form': form, 'category': category, 'shopcart':shopcart, 'total_products': total_products, 'total': total,}
    return render(request, 'contactus.html', context)


def policies8terms(request):
   setting = Setting.objects.get(pk=1)
   category = Categorie.objects.all()
   current_user = request.user
   shopcart = ShopCart.objects.filter(user_id=current_user.id)
   total_products = 0
   total = 0

   for rs in shopcart:
        total += rs.price * rs.quantity

   for rs in shopcart:
       total_products += rs.quantity
   
   
   context = {'setting':setting, 'category':category, 'shopcart':shopcart, 'total_products': total_products, 'total':total,}
   return render(request, 'policies&terms.html', context)


def customerservice(request):
    setting = Setting.objects.get(pk=1)
    category = Categorie.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_products = 0
    total = 0
    
    for rs in shopcart:
        total += rs.price * rs.quantity

    for rs in shopcart:
       total_products += rs.quantity

    context = {'setting':setting, 'category': category, 'shopcart':shopcart, 'total_products': total_products, 'total': total,}
    return render(request, 'customerservice.html', context)


def sales(request):
    #return HttpResponse('Sales')
    return HttpResponseRedirect('/')


def giftcards(request):
    #return HttpResponse('Gift Cards')
    return HttpResponseRedirect('/')


def selectLanguage(request):
    if request.method =='POST':
        cur_language = translation.get_language()
        lasturl = request.META.get('HTTP_REFERER')
        lang = request.POST['language']
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY]=lang

        return HttpResponseRedirect("/" +lang)


def category_products(request, id, slug):
    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]
    products = Product.objects.filter(category_id=id)
    category = Categorie.objects.all()
    categoryLabelName = Categorie.objects.get(pk=id)
    catdata = Categorie.objects.get(pk=id)
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_products = 0
    total = 0
    
    for rs in shopcart:
        total += rs.price * rs.quantity 

    for rs in shopcart:
       total_products += rs.quantity

    if defaultlang != currentlang:
        try:
            products = Product.objects.raw(
                'SELECT p.id,p.price,p.amount,p.image,p.variant,l.title, l.keywords, l.description,l.slug,l.detail '
                'FROM product_product as p '
                'LEFT JOIN product_productlang as l '
                'ON p.id = l.product_id '
                'WHERE p.category_id=%s and l.lang=%s', [id, currentlang])
        except:
            pass
        catdata = CategoryLang.objects.get(category_id=id, lang=currentlang)
    
    context = {'products': products,
                'category': category,
                'catdata': catdata,
                'categoryLabelName': categoryLabelName,
                'setting': setting,
                'shopcart': shopcart,
                'total_products': total_products,
                'total': total,
            }
    return render(request, 'category_products.html', context)

    #return render(request, 'aboutus.html', context)
    #return HttpResponse(products)


def product_detail(request, id, slug):
    query = request.GET.get('q')
    images = Images.objects.filter(product_id=id)
    comments = ReviewMessage.objects.filter(product_id=id)
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_products = 0
    total = 0
    total_rewiews = 0
    #total_rewiews = ReviewMessage.objects.filter(comments)

    # >>>>>>>>>>>>>>>> M U L T I   L A N G U G A E >>>>>> START
    defaultlang = settings.LANGUAGE_CODE[0:2] #en-EN
    currentlang = request.LANGUAGE_CODE[0:2]

    product = Product.objects.get(pk=id)
    category = Categorie.objects.all()

    if defaultlang != currentlang:
        try:
            prolang =  Product.objects.raw('SELECT p.id,p.price,p.amount,p.image,p.variant,l.title, l.keywords, l.description,l.slug,l.detail '
                                          'FROM product_product as p '
                                          'INNER JOIN product_productlang as l '
                                          'ON p.id = l.product_id '
                                          'WHERE p.id=%s and l.lang=%s',[id,currentlang])
            product=prolang[0]
        except:
            pass
    # <<<<<<<<<< M U L T I   L A N G U G A E <<<<<<<<<<<<<<< end
    
    
    
    '''for rev in comments:
        total_rewiews += rev.int(comments)'''
    
    total_rewiews = comments.count()

    for rs in shopcart:
        total += rs.price * rs.quantity
    
    for rs in shopcart:
       total_products += rs.quantity
    
    context = {'product': product,
                'category': category,
                'images': images,
                'comments': comments,
                'setting': setting,
                'shopcart': shopcart,
                'total_products': total_products,
                'total': total,
                'total_rewiews': total_rewiews
            }
    
    if product.variant !="None": # Product have variants
        if request.method == 'POST': # If we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id) # Selected product by click color radio
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw('SELECT * FROM product_variants WHERE product_id=%s GROUP BY size_id',[id])
            query += variant.title + 'Size:' + str(variant.size) + 'Color:' + str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id)
            sizes = Variants.objects.raw('SELECT * FROM product_variants WHERE product_id=%s GROUP BY size_id',[id])
            variant = Variants.objects.get(id=variants[0].id)

        context.update({
                        'sizes': sizes,
                        'colors': colors,
                        'variant': variant,
                        'query': query
                        })
    
    
    
    return render(request, 'product_detail.html', context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        producid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=producid, size_id=size_id)

        context = {
            'size_id': size_id,
            'producid': producid,
            'colors': colors,
        }

        data = {
            'rendered_table': render_to_string('color_list.html',
            context=context)
        }

        return JsonResponse(data)
    
    return JsonResponse(data)


def search(request):
    if request.method == 'POST':
        setting = Setting.objects.get(pk=1)
        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id=current_user.id)
        total_products = 0
        total = 0
    
        for rs in shopcart:
            total += rs.price * rs.quantity

        for rs in shopcart:
            total_products += rs.quantity
        
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get from input data
            catid = form.cleaned_data['catid']
            if catid==0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid) #SELECT * FROM product WHERE title LIKE '%query%'
            
            category = Categorie.objects.all()
            context = {
                'products': products,
                'category': category,
                'query': query,
                'setting': setting,
                'shopcart': shopcart,
                'total_products': total_products,
                'total' : total,
            }
            return render(request, 'search_products.html', context)
    
    return HttpResponseRedirect('/')


def search_auto(request): # Autocomplete textbox text fill.
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json['label'] = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def faq(request):
    category = Categorie.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_products = 0
    total = 0
    #faq = FAQ.objects.filter(status="True").order_by("ordernumber")

    defaultlang = settings.LANGUAGE_CODE[0:2]
    currentlang = request.LANGUAGE_CODE[0:2]

    for rs in shopcart:
        total += rs.price * rs.quantity
        

    for rs in shopcart:
        total_products += rs.quantity
    
    if defaultlang==currentlang:
        faq = FAQ.objects.filter(status="True",lang=defaultlang).order_by("ordernumber")
    else:
        faq = FAQ.objects.filter(status="True",lang=currentlang).order_by("ordernumber")

    context = {
        'category': category,
        'total': total,
        'total_products': total_products,
        'shopcart': shopcart,
        'faq': faq,
    }
    return render(request, "faq.html", context)


def selectcurrency(request):
    lasturl = request.META.get('HTTP_REFERER')
    if request.method == 'POST':  # check post
        request.session['currency'] = request.POST['currency']
    return HttpResponseRedirect(lasturl)


@login_required(login_url='/login') # Check login
def savelangcur(request):
    lasturl = request.META.get('HTTP_REFERER')
    curren_user = request.user
    language=Language.objects.get(code=request.LANGUAGE_CODE[0:2])
    #Save to User profile database
    data = UserProfile.objects.get(user_id=curren_user.id )
    data.language_id = language.id
    data.currency_id = request.session['currency']
    data.save()  # save data
    return HttpResponseRedirect(lasturl)


'''@login_required(login_url='/login') # Check Login
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, 'You have deleted the item from the Shopcart!')

    return redirect(request.META['HTTP_REFFERER'])'''