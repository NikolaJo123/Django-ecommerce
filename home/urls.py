from django.conf.urls import handler400, handler404
from django.urls import path, include
from . import views
from user import views as UserView

urlpatterns = [
    path('', views.index, name='index'),
    #path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
]


#handler404 = 'index.views.error_404_view'