from home.models import FAQ
from threading import current_thread
import user
from django import forms
from user.models import UserProfile
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from product.models import Categorie, ReviewMessage
from order.models import Order, OrderProduct, ShopCart
from user.forms import SignUp_Form, UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile, UserFavourites, UserFavouritesForm
from product.models import Product
from django.utils.translation import gettext as _



# Create your views here.

@login_required(login_url='/login')
def index(request):
    category = Categorie.objects.all()
    current_user = request.user # Access User Session Information.
    profile = UserProfile.objects.get(user_id=current_user.id)
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_products = 0
    total = 0

    for rs in shopcart:
        total += rs.price * rs.quantity

    for rs in shopcart:
        total_products += rs.quantity

    context = {
        'category': category,
        'profile': profile,
        'shopcart': shopcart,
        'total_products': total_products,
        'total': total,
    }
    return render(request, 'user_profile.html', context)




def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user =request.user
            userprofile=UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            return HttpResponseRedirect('/') # Redirect to a success page.
        else:
            messages.warning(request, "Login Error!! Username or Password is incorrect.")
            return HttpResponseRedirect('/login')
            # Return an 'invalid' login error message.

    current_user = request.user
    #images = UserProfile.objects.get(user_id=current_user.id)
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_products = 0
    total = 0
    category = Categorie.objects.all()

    for rs in shopcart:
        if rs.variant == None:
            total = rs.amount
        else:
            total = rs.varamount

    for rs in shopcart:
        total_products += rs.quantity

    context = {
        'category': category,
        'total_products': total_products,
        'total' : total,
        'shopcart': shopcart,
    }
    return render(request, 'login.html', context)
    #return HttpResponse("Login Page")



def signup_form(request):
    if request.method == 'POST':
        form = SignUp_Form(request.POST)
        if form.is_valid():
            form.save() #completed sign up
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image = 'images/users/user.png'
            data.save()
            messages.success(request, "Your account has been created!")

            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')
    
    form = SignUp_Form()
    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)
    #return HttpResponse("Signup Page")



def logout_form(request):
    url = request.META.get('HTTP_REFERER')
    logout(request)
    return HttpResponseRedirect("/")



def user_panel_form(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_products = 0
    total = 0
    category = Categorie.objects.all()

    for rs in shopcart:
        total += rs.price * rs.quantity

    for rs in shopcart:
        total_products += rs.quantity

    context = {
        'category': category,
        'total_products': total_products,
        'total' : total,
        'shopcart': shopcart,
    }
    return render(request, 'user_profile.html', context)




@login_required(login_url='/login') # Check Login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user data
        # "instance=request.user.userprofile" comes from "userprofile" model -> OneToOneField relation.
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Categorie.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id=current_user.id)
        total_products = 0
        total = 0

        for rs in shopcart:
            total += rs.price * rs.quantity

        for rs in shopcart:
            total_products += rs.quantity

        context = {
            'category': category,
            'total': total,
            'total_products': total_products,
            'shopcart': shopcart,
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'user_update.html', context)



@login_required(login_url='/login') # Check Login
def user_password_update(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # Important!
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, "Please correct the error below.<br>" +str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id=current_user.id)
        total_products = 0
        total = 0
        category = Categorie.objects.all()
        form = PasswordChangeForm(request.user)

        for rs in shopcart:
            total += rs.price * rs.quantity

        for rs in shopcart:
            total_products += rs.quantity

        return render(request, 'user_password_update.html', {
            'form': form,
            'category': category,
            'total': total,
            'total_products': total_products,
            'shopcart': shopcart,
        })


def user_orders(request):
        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id=current_user.id)
        total_products = 0
        total = 0
        category = Categorie.objects.all()
        #form = PasswordChangeForm(request.user)
        orders = Order.objects.filter(user_id=current_user.id).order_by('created_at').reverse()

        for rs in shopcart:
            total += rs.price * rs.quantity

        for rs in shopcart:
            total_products += rs.quantity

        return render(request, 'user_orders.html', {
            #'form': form,
            'category': category,
            'orders': orders,
            'total': total,
            'total_products': total_products,
            'shopcart': shopcart,
        })



@login_required(login_url='/login') # Check login
def user_orderdetail(request, id):
    category = Categorie.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_products = 0
    total = 0
    #order_id = request.Order.id
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)

    for rs in shopcart:
        total += rs.price * rs.quantity

    for rs in shopcart:
        total_products += rs.quantity

    context = {
        'category': category,
        'total': total,
        'total_products': total_products,
        'shopcart': shopcart,
        'orderitems': orderitems,
        'order': order,
    }
    return render(request, "user_order_detail.html", context)



@login_required(login_url='/login') # Check login
def user_orders_product(request):
    category = Categorie.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_products = 0
    total = 0
    user_order_product = OrderProduct.objects.filter(user_id=current_user.id)

    for rs in shopcart:
        total += rs.price * rs.quantity

    for rs in shopcart:
        total_products += rs.quantity

    context = {
        'category': category,
        'total': total,
        'total_products': total_products,
        'shopcart': shopcart,
        'user_order_product': user_order_product,
    }
    return render(request, "user_order_products.html", context)


@login_required(login_url='/login') # Check login
def user_order_product_detail(request, id, oid):
    category = Categorie.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_products = 0
    total = 0
    order= Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id, user_id=current_user.id)

    for rs in shopcart:
        total += rs.price * rs.quantity

    for rs in shopcart:
        total_products += rs.quantity

    context = {
        'category': category,
        'total': total,
        'total_products': total_products,
        'shopcart': shopcart,
        'order': order,
        'orderitems': orderitems
    }
    return render(request, "user_order_detail.html", context)



@login_required(login_url='/login') # Check login
def user_comments(request):
    category = Categorie.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_products = 0
    total = 0
    comments = ReviewMessage.objects.filter(user_id=current_user.id)

    for rs in shopcart:
        total += rs.price * rs.quantity

    for rs in shopcart:
        total_products += rs.quantity

    context = {
        'category': category,
        'total': total,
        'total_products': total_products,
        'shopcart': shopcart,
        'comments': comments,
    }
    return render(request, "user_comments.html", context)



@login_required(login_url='/login') # Check Login
def addtofavourites(request, id):
    #return HttpResponse('Added to Favourites!')
    last_url = request.META.get('HTTP_REFERER') #get last url
    current_user = request.user # Access User Session information
    product= Product.objects.get(pk=id)
    variantid = request.POST.get('variantid')  # from variant add to favourites


    '''chechproduct = UserFavourites.objects.filter(product_name_id=id) # Check product in favourites
    if chechproduct:
        control = 1 # The product is in favourites
    else:
        control = 0 # The product is not in favourites

    if product.variant != 'None':
        
        checkinvariant = UserFavourites.objects.filter(variant_id=variantid, user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1 # The product is in favourites
        else:
            control = 0 # The product is not in favourites""
    else:
        checkinproduct = UserFavourites.objects.filter(product_name_id=id, user_id=current_user.id) # Check product in shopcart
        if checkinproduct:
            control = 1 # The product is in favourites
        else:
            control = 0 # The product is not in favourites"""
            '''
    checkinproduct = UserFavourites.objects.filter(product_name_id=id, user_id=current_user.id) # Check product in favourites
    if checkinproduct:
        control = 1 # The product is in favourites
    else:
        control = 0 # The product is not in favourites"""
    
    if request.method == 'POST': # if there is a post
        form = UserFavouritesForm(request.POST)
        if form.is_valid():
            if control==1: # Insert to Favourites
                if product.variant == None:
                    data = UserFavourites.objects.get(product_name_id=id, user_id=current_user.id)
                else:
                    data = UserFavourites.objects.get(variant_id=variantid, product_name_id=id, user_id=current_user.id)

                #data.quantity += form.cleaned_data['quantity']
                messages.success(request, "Product is already in Favourites! Check your Favourites list in your account page to view all your favourites.")
            else: #
                data = UserFavourites()
                data.user_id = current_user.id
                data.product_name_id = id
                data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
                messages.success(request, 'Product added to Favourites.')
        return HttpResponseRedirect(last_url)

    else: # if there is no post
        if control == 1:
            data = UserFavourites.objects.get(product_name_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()
            messages.success(request, "Product is already in Favourites! Check your Favourites list in your account page to view all your favourites.")
        else: # Insert to Favourites
            data = UserFavourites()
            data.user_id = current_user.id
            data.product_name_id = id
            data.quantity = 1
            data.variant_id = None
            data.save()
            messages.success(request, 'Product added to Favourites.')
        return HttpResponseRedirect(last_url)




@login_required(login_url='/login') # Check login
def user_favourites(request):
    category = Categorie.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total_products = 0
    total = 0
    favourite = UserFavourites.objects.filter(user_id=current_user.id)

    for rs in shopcart:
        total += rs.price * rs.quantity

    for rs in shopcart:
        total_products += rs.quantity

    context = {
        'category': category,
        'total': total,
        'total_products': total_products,
        'shopcart': shopcart,
        'favourite': favourite,
    }
    return render(request, "favourites.html", context)


@login_required(login_url='/login') # Check Login
def deletefromvafourites(request, id):
    url = request.META.get('HTTP_REFERER') #get last url
    current_user = request.user


    UserFavourites.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'You have deleted the item from your Favourites list!')

    return HttpResponseRedirect(url)



@login_required(login_url='/login') # Check login
def user_deletecomment(request, id):
    current_user = request.user
    ReviewMessage.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Your comment has been deleted!')
    return HttpResponseRedirect('/user/comments')



