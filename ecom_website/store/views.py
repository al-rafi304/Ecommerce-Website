from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Shop
from .forms import ShopForm, ProductForm
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
        messages.error(request, 'You do not have the permission to view that page')
        return redirect('home')
    if request.user.is_seller:                      # Already owns shop
        messages.error(request, 'You already own a shop and cannot create any more')
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

def shop(request, shop_id):
    my_shop = Shop.objects.get(pk = shop_id)
    products = my_shop.product_set.all()
    return render(request, 'store/shop.html', {
        'shop': my_shop,
        'products': products
        })

def product(request, product_id):
    product = Product.objects.get(pk = product_id)
    return render(request, 'store/product.html', {'product': product})

def add_product(request, shop_id):

    if request.user.is_authenticated == False or request.user.is_seller == False or request.user.shop.pk != shop_id:
        messages.error(request, 'You do not have the permission to view that page')
        return redirect('home')


    my_shop = Shop.objects.get(pk = shop_id)
    products = my_shop.product_set.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = my_shop
            form.save()

            messages.success(request, 'Product has been added to your shop!')
            return render(request, 'store/shop.html', {
                'shop': my_shop,
                'products': products
            })
            
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})

    