from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import stripe
import time
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from .models import Product, Shop, Cart, Cart_item, Order, Order_item
from .forms import ShopForm, ProductForm


STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY
stripe.api_key = STRIPE_SECRET_KEY


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

            try:
                account = stripe.Account.create(
                    type='express',
                    country='US',
                    email=request.user.email,
                    capabilities={
                        'card_payments': {'requested': True},
                        'transfers': {'requested': True},
                    }
                )

                # Store the account ID in the database
                shop.stripe_account_id = account.id
                shop.save()

                messages.success(request, 'Congratulations! You created you own shop!')
                return redirect('home')
            
            except stripe.error.StripeError as e:
                messages.error(request, str(e))
                return render(request, 'create_shop.html')


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

def checkout(request):
    user = request.user
    cart = user.cart
    cart_items = Cart_item.objects.filter(cart=cart)
    checkout_items = {}
    total_price = 0

    for item in cart_items:
        shop_id = item.product.shop.id
        if shop_id not in checkout_items:
            checkout_items[shop_id] = []
        checkout_items[shop_id].append(item)
        total_price += item.product.price * item.quantity

    line_items = []
    for shop_id, items in checkout_items.items():
        for item in items:
            line_items.append({
                # 'name': item.product.title,
                # 'amount': int(item.product.price * 100),
                # 'currency': 'usd',
                'quantity': item.quantity,

                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(item.product.price * 100),
                    'product_data': {
                        'name': item.product.title,
                        'description': item.product.description,
                        # 'images': [item.product.image]
                    }
                }
            })

    transfers = []
    for shop in checkout_items.keys():
        amount = 0
        for item in checkout_items[shop]:
            amount += item.product.price * item.quantity
        transfers.append({
            'destination': shop,
            'amount': amount
        })

    item = cart_items[0]
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url= 'http://127.0.0.1:8000/',#'http://example.com/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url= 'http://127.0.0.1:8000/cart', #'http://example.com/cancel',
    )

    # for transfer in transfers:
    #     dest = Shop.objects.get(id=transfer['destination']).stripe_account_id
    #     stripe.Transfer.create(
    #         amount=int(transfer['amount']),
    #         currency='USD',
    #         destination=dest
    #     )

    # print(f'\nItems: {checkout_items}\nTotal Price: {total_price}\nLine_items: {line_items}\n{transfers}\n')
    print(f'\n{item.product.image}\n')
    return redirect(session.url, code=303)


    