from django.conf.urls import handler400, handler404
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.user_password_update, name='user_password_update'),
    path('orders/', views.user_orders, name='user_orders'),
    path('orders_product/', views.user_orders_product, name='user_orders_product'),
    path('orderdetail/<int:id>', views.user_orderdetail, name='user_orderdetail'),
    path('order_product_detail/<int:id>/<int:oid>', views.user_order_product_detail, name='user_order_product_detail'),
    path('comments/', views.user_comments, name='user_comments'),
    path('favourites/', views.user_favourites, name='user_favourites'),
    path('addtofavourites/<int:id>', views.addtofavourites, name='addtofavourites'),
    path('deletefromvafourites/<int:id>', views.deletefromvafourites, name='deletefromvafourites'),
    path('deletecomment/<int:id>', views.user_deletecomment, name='user_deletecomment'),
    #path('logout/', views.logout_form, name='logout_form'),

]