#from product.models import Categorie
#import product
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from order.models import Order, OrderForm, OrderProduct, ShopCartForm, ShopCart
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
#from django.contrib.auth.models import User
from product.models import Categorie, Product, Images, Variants
from home.models import Setting
from product.models import Categorie
from user.models import UserProfile





# Create your views here.

def index(request):
    return HttpResponse("Order Page")


@login_required(login_url='/login') # Check Login
def addtoshopcart(request, id):
    url = request.META.get('HTTP_REFERER') #get last url
    current_user = request.user # Access User Session information
    product= Product.objects.get(pk=id)
    variantid = request.POST.get('variantid')  # from variant add to cart


    chechproduct = ShopCart.objects.filter(product_id=id) # Check product in shopcart
    if chechproduct:
        control = 1 # The product is in the cart
    else:
        control = 0 # The product is not in the cart

    if product.variant != 'None':
        
        checkinvariant = ShopCart.objects.filter(variant_id=variantid, user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""
    else:
        checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id) # Check product in shopcart
        if checkinproduct:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""
    
    if request.method == 'POST': # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1: # Update shopcart
                if product.variant == 'None':
                    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                else:
                    data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)

                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save() # Save data
            else: # Insert to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Shopcart.")
        return HttpResponseRedirect(url)

    else: # if there is no post
        if control == 1: # Update shopcart
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else: # Update to Shopcart
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.variant_id =None
            data.save()
        messages.success(request, 'Product added to Shopcart.')
        return HttpResponseRedirect(url)

    #return  HttpResponse(str(id))


def shopcart(request):
    category = Categorie.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    shoppingcart = ShopCart.objects.filter(user_id=current_user.id)
    setting = Setting.objects.get(pk=1)
    total = 0
    qnt = 0 # single product quantity.
    total_products = 0

    for rs in shopcart:
        total += rs.price * rs.quantity
    
    for rs in shoppingcart:
        total_products += rs.quantity

    context = { 'shopcart': shopcart,
                'shoppingcart': shoppingcart,
                'category': category,
                'setting': setting,
                'total' : total,
                'total_products': total_products
                }
    return render(request, 'shopcart_products.html', context)


@login_required(login_url='/login') # Check Login
def deletefromcart(request, id):
    url = request.META.get('HTTP_REFERER') #get last url
    current_user = request.user


    ShopCart.objects.filter(id=id).delete()
    messages.success(request, 'You have deleted the item from the Shopcart!')

    return HttpResponseRedirect(url)



def upgshopcart(request, id):
    last_url = request.META.get('HTTP_REFERER')
    data = ShopCart.objects.get(product_id=id)
    product = Product.objects.get(id=id)

    if data.quantity == product.amount:
        messages.info(request, "Can't add more products than whats already in stock!")
    else:
        data.quantity += 1
    
    data.save()

    return HttpResponseRedirect(last_url)


def dcrshopcart(request, id):
    last_url = request.META.get('HTTP_REFERER')
    data = ShopCart.objects.get(product_id=id)
    #product = Product.objects.get(product_id=id)
    
    if data.quantity < 1:
        messages.info(request, 'Your product quantity value is already 0!')
    else:
        data.quantity -= 1
    
    data.save()

    return HttpResponseRedirect(last_url)



def orderproduct(request):
    category = Categorie.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    shoppingcart = ShopCart.objects.filter(user_id=current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    setting = Setting.objects.get(pk=1)
    total = 0
    total_products = 0

    for rs in shopcart:
        total += rs.price * rs.quantity
    
    for rs in shoppingcart:
        total_products += rs.quantity    
    
    url = request.META.get('HTTP_REFERER') #get last url
    if total_products < 1:
        messages.success(request, "Your cart is empty. Can't proceed with payment!")
        return HttpResponseRedirect(url)
    else:

        if request.method == 'POST': #If there is a post
            form = OrderForm(request.POST)
            if form.is_valid():
                # Send Credit card to bank, If the bank responds ok, continue, if not, hsow the error.

                data = Order()
                data.first_name = form.cleaned_data['first_name'] # get product quantity from form
                data.last_name = form.cleaned_data['last_name']
                data.address = form.cleaned_data['address']
                data.city = form.cleaned_data['city']
                data.country = form.cleaned_data['country']
                data.phone = form.cleaned_data['phone']
                data.user_id = current_user.id
                data.total = total
                data.ip = request.META.get('REMOTE_ADDR')
                ordercode = get_random_string(5).upper() # Random code
                data.code = ordercode
                data.save()

                # Move Shopping cart items to Order Products items

                for rs in shoppingcart:
                    detail = OrderProduct()
                    detail.order_id     = data.id # Order Id
                    detail.product_id   = rs.product_id
                    detail.user_id      = current_user.id
                    detail.quantity     = rs.quantity
                    
                    if rs.product.variant == 'None':
                        detail.price    = rs.product.price
                    else:
                        detail.price = rs.variant.price
                        
                    detail.variant_id   = rs.variant_id
                    detail.amount        = rs.amount
                    detail.save()

                    # ***Reduce quantity of sold product from Amount of Product

                    if  rs.product.variant=='None':
                        product = Product.objects.get(id=rs.product_id)
                        product.amount -= rs.quantity
                        product.save()
                    else:
                        product = Product.objects.get(id=rs.product_id)
                        variant = Variants.objects.get(id=rs.variant_id)
                        variant.quantity -= rs.quantity
                        product.amount -= rs.quantity
                        variant.save()
                        product.save() 

                ShopCart.objects.filter(user_id=current_user.id).delete() # Clear & delete shopcart
                request.session['cart_items'] = 0
                messages.success(request, 'Your Order has been completed. Thank you for your interest.')
                return HttpResponseRedirect("/order/orderconfiramation/" + str(detail.order_id))
                
                    
            else:
                messages.warning(request, form.errors)
                return HttpResponseRedirect("/order/orderproduct")
            
        

        form = OrderForm()

        context = { 'shopcart': shopcart,
                    'shoppingcart': shoppingcart,
                    'category': category,
                    'setting': setting,
                    'total' : total,
                    'total_products': total_products,
                    'profile': profile,
                    }
        return render(request, 'Order_Form.html', context)


def orderconfiramation(request, id):
    current_user = request.user
    category = Categorie.objects.all()
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    data = Order.objects.get(id=id, user=current_user.id)
    ordercode = data.code
    total = 0
    total_products = 0

    for rs in shopcart:
        total += rs.price * rs.quantity
    
    for rs in shopcart:
        total_products += rs.quantity

    return render(request, 'Order_Completed.html',{'ordercode': ordercode, 'category': category,
                                                    'total':total, 'total_products': total_products,  })
