"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
import home
from home import views
#from product import views as ProductView
from order import views as OrderView
from user import views as UserView
from django.utils.translation import gettext_lazy as _


urlpatterns = [
    path('selectLanguage', views.selectLanguage, name='selectLanguage'),
    path('selectcurrency', views.selectcurrency, name='selectcurrency'),
    path('savelangcur', views.savelangcur, name='savelangcur'),
    path('i18n/', include('django.conf.urls.i18n')),
]


urlpatterns += i18n_patterns(
    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('order/', include('order.urls')),
    path('user/', include('user.urls')),
    path('currencies/', include('currencies.urls')),
    path('jet', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    
    path(_('aboutus/'), views.aboutus, name='aboutus'),
    path(_('contactus/'), views.contactus, name='contactus'),
    path('policies&terms/', views.policies8terms, name='policies&terms'),
    path('customerservice/', views.customerservice, name='customerservice'),
    path('sales/', views.sales, name='sales'),
    path('giftcards/', views.giftcards, name='giftcards'),

    #path('checkout/', views.checkout, name='checkout'),

    path('product/', include('product.urls')),
    path('category/<int:id>/<slug:slug>', views.category_products, name='category_products'),

    path(_('admin/'), admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('search/', views.search, name='search'),
    path('search_auto/', views.search_auto, name='search_auto'),
    path('product/<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
    path('shopcart/', OrderView.shopcart, name='shopcart'),
    path('login/', UserView.login_form, name='login_form'),
    path('logout/', UserView.logout_form, name='logout_form'),
    path('logout/', include('user.urls')),
    path('signup/', UserView.signup_form, name='signup_form'),
    path('faq/', views.faq, name='faq'),
    #path('ajaxtest/', views.ajaxtest, name='ajaxtest'),
    #path('ajaxpost/', views.ajaxpost, name='ajaxpost'),
    path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),
    prefix_default_language = False

    #path('user_panel/', UserView.user_panel_form, name='user_panel_form'),
 ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""if settings.DEBAG: #new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"""
    
