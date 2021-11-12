from collections import namedtuple
from django.urls import path, include
from . import views
from user import views as UserView

urlpatterns = [
    path('', views.index, name='index'),
    path('addtoshopcart/<int:id>', views.addtoshopcart, name='addtoshopcart'),
    path('upgshopcart/<int:id>', views.upgshopcart, name='upgshopcart'),
    path('dcrshopcart/<int:id>', views.dcrshopcart, name='dcrshopcart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('orderproduct', views.orderproduct, name='orderproduct'),
    path('orderconfiramation/<int:id>', views.orderconfiramation, name='orderconfiramation'),
]