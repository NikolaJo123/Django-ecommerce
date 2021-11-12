from django import contrib
from django.contrib import messages
from django.db.models.query import RawQuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
#from home import templates
from home.views import product_detail
from product.models import Comment_ReviewForm, ReviewMessage
from home.models import MessageAlert, Setting




# Create your views here.

def index(request):
   #context = product_detail.
   return render(request,'category_products.html')
   #return HttpResponse('Hello world!')


def addcomment(request, id):
   url =request.META.get('HTTP_REFERER') # get last url
   #return HttpResponse(url) # -> This is just for checking if it gets the same url and the rest of the code will not be executed.
   comment_review = MessageAlert.objects.get()
   if request.method == 'POST': # Check post.
        form = Comment_ReviewForm(request.POST) 
        if form.is_valid():
            data = ReviewMessage() # Create relation with model.
            data.name = form.cleaned_data['name'] # Get form input data.
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = id
            current_user = request.user
            data.user_id = current_user
            data.save() # Save data to table
            messages.success(request, comment_review)
            return HttpResponseRedirect(url)
   

   #context = {'setting': Setting, 'form': form}
   return HttpResponseRedirect(url)