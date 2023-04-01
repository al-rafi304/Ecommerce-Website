from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Product, Shop, Cart, Cart_item, Order, Order_item
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

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart_obj = Cart.objects.get(member=user)
        cart_items = Cart_item.objects.filter(cart=cart_obj)        # SELECT * FROM Cart_item WHERE cart=cart_obj
        return render(request, 'store/cart.html', {
            'cart_items': cart_items,
            'user': user,
        })
    else:
        messages.error(request, 'You do not have the permission to view that page!')
        return redirect('home')

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_pk = request.POST.get('product_pk')
        product_quantity = request.POST.get('product_quantity')
        product_obj = Product.objects.get(pk=product_pk)
        print('\n' + str(Product.objects.get(pk=product_pk)) + '\n')

        cart_obj = Cart.objects.get(member = request.user.pk)
        user = request.user.pk
        cart_item = Cart_item.objects.create(cart=cart_obj, product=product_obj, quantity=product_quantity)
        cart_item.save()

        response_data = {'something': product_pk}
        return JsonResponse(response_data)
    else:
        print("\nSOMETHING WENT WRONGE\n")


    