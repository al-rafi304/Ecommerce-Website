from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Shop
from .forms import ShopForm
# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(
        request, 'store/home.html',
        {
            'Products': products,
            'request': request,
        }
        )

def create_shop(request):

    # Permission handling
    if request.user.is_authenticated == False:      # Not authenticated
        messages.success(request, 'You do not have the permission to view that page')
        return redirect('home')
    if request.user.is_seller:                      # Already owns shop
        messages.success(request, 'You already own a shop and cannot create any more')
        return redirect('home')

    # View handling
    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            shop = form.save(commit=False)  # Creating shop instance without saving in database
            shop.owner = request.user       # Adding foreign key
            form.save()                     # Saving in database

            request.user.is_seller = True
            request.user.save()

            messages.success(request, 'Congratulations! You created you own shop!')
            return redirect('home')
    else:
        form = ShopForm()
    return render(request, 'store/create_shop.html', {'form': form})