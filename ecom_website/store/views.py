from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import stripe
import random
import csv
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from .models import Product, Shop, Cart, Cart_item, Order, Order_item, Transaction
from .forms import ShopForm, ProductForm


STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY
stripe.api_key = STRIPE_SECRET_KEY


# Create your views here.

def home(request):
    products = Product.objects.all()                                                        # SELECT * FROM Product
    shops = Shop.objects.all()                                                              # SELECT * FROM Shop
    display_shops = Shop.objects.exclude(Q(banner_img='') | Q(banner_img__isnull=True))     # SELECT * FROM Shop WHERE banner_img IS NOT NULL OR banner_img!='';
    print(f'\n\n{display_shops}\n\n')

    display_shop_list = list(display_shops)
    shops_list = list(shops)
    product_list = list(products)

    # Randomly suffling 
    random.shuffle(shops_list)      
    random.shuffle(product_list)
    random.shuffle(display_shop_list)

    return render(
        request, 'store/home.html',
        {
            'Products': product_list[:9],
            'shops': shops_list[:4],
            'display_shops': display_shop_list,
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
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)  # Creating shop instance without saving in database
            shop.owner = request.user       # Adding foreign key
            form.save()                     # Saving in database                                        INSERT INTO Shop VALUES (form.data)

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
                shop.save()                                                                             # INSERT INTO Shop SHOP (stripe_account_id) VALUES (account.id)

                messages.success(request, 'Congratulations! You created you own shop!')
                return redirect('home')
            
            except stripe.error.StripeError as e:
                messages.error(request, str(e))
                return render(request, 'store/shop_form.html')


    else:
        form = ShopForm()
    return render(request, 'store/shop_form.html', {
        'form': form,
        'purpose': 'Create'
        })

def shop(request, shop_id):
    my_shop = Shop.objects.get(pk = shop_id)            # SELECT * FROM Shop WHERE id=shop_id
    products = my_shop.product_set.all()                # SELECT * FROM Product WHERE shop=my_shop
    return render(request, 'store/shop.html', {
        'shop': my_shop,
        'products': products
        })

def product(request, product_id):
    product = Product.objects.get(pk = product_id)                          # SELECT * FROM Product WHERE id=product_id
    cart_items = Cart_item.objects.filter(cart=request.user.cart)           # SELECT * FROM Cart_item WHERE cart=request.user.cart
    in_cart = False
    for item in cart_items:
        if item.product == product:
            in_cart = True
            break

    print(in_cart)
    return render(request, 'store/product.html', {
        'product': product,
        'in_cart': in_cart
        })

def add_product(request, shop_id):

    if request.user.is_authenticated == False or request.user.is_seller == False or request.user.shop.pk != shop_id:
        messages.error(request, 'You do not have the permission to view that page')
        return redirect('home')


    my_shop = Shop.objects.get(pk = shop_id)                                        # SELECT * FROM Shop WHERE id=shop_id
    products = my_shop.product_set.all()                                            # SELECT * FROM Product WHERE shop=shop_id
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = my_shop
            form.save()                                                             # INSERT INTO Product VALUES (form.data)

            messages.success(request, 'Product has been added to your shop!')
            return redirect('manage_products', shop_id=shop_id)
            
    else:
        form = ProductForm()
    return render(request, 'store/product_form.html', {
        'form': form,
        'button_txt': 'Add'
        })

def update_product(request, product_id):

    product = Product.objects.get(id=product_id)                                # SELECT * FROM Product WHERE id=product_id
    form = ProductForm(instance=product)

    if request.user.shop.id != product.shop.id:
        raise Http404("Page not found")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()                                                         # UPDATE Product SET title=form.title, shop=form.shop... WHERE id=product_id

            messages.success(request, 'Product has been updated!')
            return redirect('manage_products', shop_id=product.shop.id)



    return render(request, 'store/product_form.html', {
        'form': form,
        'button_txt': 'Update'
        })

def cart(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            item_id = request.POST['item_id']
            print(item_id)
            Cart_item.objects.get(id=item_id).delete()              # DELETE FROM Cart_item WHERE id=item_id
            return redirect('cart')


        user = request.user
        cart_obj = Cart.objects.get(member=user)                    # SELECT * FROM Cart WHERE member=user
        cart_items = Cart_item.objects.filter(cart=cart_obj)        # SELECT * FROM Cart_item WHERE cart=cart_obj
        
        total_price = 0                             # Total price of cart
        items = []                                  # Has Product item and total price of cart item
        for item in cart_items:
            temp = {}
            temp['item'] = item
            temp['total_price'] = item.product.price * item.quantity
            total_price += item.product.price * item.quantity
            items.append(temp)
        return render(request, 'store/cart.html', {
            'cart_items': items,
            'user': user,
            'total_price': total_price
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

        cart_obj = Cart.objects.get(member = request.user.pk)                                                       # SELECT * FROM Cart WHERE member=request.user.pk
        cart_item = Cart_item.objects.create(cart=cart_obj, product=product_obj, quantity=product_quantity)         # INSERT INTO Cart_item (cart, product, quantity) VALUES (cart_obj, product_obj, product_quantity)
        cart_item.save()

        return redirect('product', product_id = product_pk)
    else:
        print("\nSOMETHING WENT WRONGE\n")

def checkout(request):
    user = request.user
    cart = user.cart
    cart_items = Cart_item.objects.filter(cart=cart)                    # SELECT * FROM Cart_item WHERE cart=cart
    checkout_items = {}
    total_price = 0

    # Finding cart items
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

    # Making the payment
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url= 'http://127.0.0.1:8000/checkout/{CHECKOUT_SESSION_ID}/success',#'http://example.com/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url= 'http://127.0.0.1:8000/cart', #'http://example.com/cancel',
    )

    return redirect(session.url, code=303)

def checkout_success(request, session_id):
    session = stripe.checkout.Session.retrieve(session_id)
    print("session: ", session)
    total = session.amount_total
    transaction_id = session.payment_intent
    cart = request.user.cart
    cart_items = Cart_item.objects.filter(cart=cart)                            # SELECT * FROM Cart_item WHERE cart=user.cart.id

    # Making sure records are not added twice
    if Transaction.objects.filter(stripe_trx_id=transaction_id).exists():       # SELECT * FROM Transaction WHERE stripe_trx_id = transaction_id
        raise Http404('Error page not found')

    # Getting all items which were checked out
    checkout_items = {}
    for item in cart_items:
        shop_id = item.product.shop
        if shop_id not in checkout_items:
            checkout_items[shop_id] = []
        checkout_items[shop_id].append(item)

    # Saving Order, Order_item, Transaction for each shop
    for shop, items in checkout_items.items():
        order = Order(member=request.user, shop=shop)                       
        order.save()                                                            # INSERT INTO Order (member, shop) VALUES (request.user, shop)
        temp_amount = 0
        for item in items:
            instance = Order_item(
                product=item.product,
                  order=order,
                    quantity=item.quantity
            )
            instance.save()                                                     # INSERT INTO Order_item (product, order, quantity) VALUES (item,product, order, item.quantity)
            temp_amount += item.product.price

            # Updating stock/sold
            product_instance = Product.objects.get(id=item.product.id)          # SELECT * FROM Product WHERE id=product.id
            product_instance.stock -= item.quantity
            product_instance.sold += item.quantity
            product_instance.save()                                             # UPDATE Product SET stock = stock-item.quantity, sold = sold+item.quantity WHERE id=item.product.id

        trx_instance = Transaction(
            amount = temp_amount,
            order = order,
            member = request.user,
            stripe_trx_id = transaction_id
        )
        trx_instance.save()                                                     # INSERT INTO Transaction (amount, order, member, stripe_trx_id) VALUES (temp_amount, order, request.user, transaction_id)
    
    # Emptying cart
    for item in cart_items:
        item.delete()                                                           # DELECT FROM Cart_item WHERE cart=request.user.cart

    return render(request, 'store/checkout_success.html', {
        'trx': transaction_id,
        'total': total/100
    })

def my_orders(request):
    orders_obj = Order.objects.filter(member=request.user).order_by('-created_at')      # SELECT * FROM Order WHERE member=request.user ORDER BY created_at DESC

    orders = []

    for order in orders_obj:
        order_dict = {}
        order_dict['order'] = order
        order_dict['total'] = 0
        order_dict['trx'] = Transaction.objects.get(order=order)                        # SELECT * FROM Transaction WHERE order=order      
        order_dict['products'] = []

        for order_item in Order_item.objects.filter(order=order):                       # SELECT * FROM Order_item WHERE order=order
            title = order_item.product.title
            price = order_item.product.price
            quantity = order_item.quantity
            item = {'title': title, 'quantity': quantity}
            order_dict['products'].append(item)
            order_dict['total'] += price * quantity

        orders.append(order_dict)
    
    print(f"\n\n{orders}\n\n")


    return render(request, 'store/my_orders.html', {
        'orders': orders
    })

def shop_orders(request, shop_id):

    if not request.user.is_seller or not request.user.shop.id == shop_id:
        raise Http404('Error page not found')
    
    shop = Shop.objects.get(id=shop_id)                                         # SELECT * FROM Shop WHERE id=shop_id
    orders_obj = Order.objects.filter(shop=shop).order_by('-created_at')        # SELECT * FROM Order WHERE shop=shop ORDER BY created_at DESC

    if request.method == "POST":
        order_id = request.POST['order_id']
        order_status = request.POST['status']
        order_instance = Order.objects.get(id=order_id)                         # SELECT * FROM Order WHERE id=order_id
        order_instance.order_status = order_status
        order_instance.save()                                                   # INSERT INTO Order SET order_status=order_status WHERE id=order_id

        return redirect('shop_orders', shop_id=shop_id)

    orders = []
    order_count = {
        'total_count': 0,
        'delivered_count': 0,
        'pending_count': 0,
        'cancelled_count': 0,
    }
    

    for order in orders_obj:
        order_dict = {}
        order_dict['order'] = order
        order_dict['total'] = 0
        order_dict['products'] = []

        for order_item in Order_item.objects.filter(order=order):   #SELECT * FROM Order_item WHERE order=order
            title = order_item.product.title
            price = order_item.product.price
            quantity = order_item.quantity
            item = {'title': title, 'quantity': quantity}
            order_dict['products'].append(item)
            order_dict['total'] += price * quantity

        orders.append(order_dict)

        order_count['total_count'] += 1
        if order.order_status == order.DELIVERED:
            order_count['delivered_count'] += 1
        if order.order_status == order.PENDING:
            order_count['pending_count'] += 1
        if order.order_status == order.CANCELLED:
            order_count['cancelled_count'] += 1


    return render(request, 'store/shop_orders.html', {
        'orders': orders,
        'order_count': order_count
    })

def download_order(request, shop_id):
    print('sdfsdf')
    if request.user.shop.id != shop_id:
        raise Http404("Page not found")
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=orders.csv'

    shop = Shop.objects.get(id=shop_id)                                     # SELECT * FROM Shop WHERE id=shop_id
    orders = []
    orders_inst = Order.objects.filter(shop=shop)                           # SELECT * FROM Order WHERE shop=shop

    for order in orders_inst:
        member = order.member
        member.first_name
        temp = {}
        temp['order'] = order
        temp['user'] = member
        temp['items'] = []
        temp['total'] = 0
        for item in Order_item.objects.filter(order=order):                 # SELECT * FROM Orde_item WHERE order=order
            temp['items'].append({
                'product': item.product.title,
                'quantity': item.quantity
            })
            temp['total'] += item.product.price * item.quantity
        orders.append(temp)

        print(orders)

    # CSV writer
    writer = csv.writer(response)

    # Writing Headers
    writer.writerow([
        'Order ID',
        'Placed At',
        'Order From',
        'Shipping Address',
        'Email',
        'Phone',
        'Products',
        'Total',
        'Status'
    ])

    # Writing each row
    for order in orders:
        writer.writerow([
            order['order'].id,
            order['order'].created_at,
            f"{order['user'].first_name} {order['user'].last_name}",
            order['user'].address,
            order['user'].email,
            order['user'].phone,
            order['items'],
            f"${order['total']}",
            order['order'].order_status
        ])

    return response

def manage_products(request, shop_id):

    if not request.user.is_seller:
        raise Http404("Page not found")
    elif request.user.shop.id != shop_id:
        raise Http404("Page not found")

    shop = Shop.objects.get(id=shop_id)                                         # SELECT * FROM Shop WHERE id=shop_id
    products = Product.objects.filter(shop=shop)                                # SELECT * FROM Product WHERE shop=shop


    # Deleting product
    if request.method == 'POST':
        product = Product.objects.get(id = request.POST['product_id'])          
        product.delete()                                                        # DELETE FROM Product WHERE id=request.POST['product_id']
        
        return redirect('manage_products', shop_id=shop_id)

    return render(request, 'store/manage_products.html', {
        'products': products
    })

def all_products(request):

    searched = False
    query = request.GET.get('search')

    if  query != None:
        products = Product.objects.filter(title__contains=query)        # SELECT * FROM Product WHERE title LIKE %query%
        searched = True
    else:
        products = Product.objects.all()                                # SELECT * FROM Product
    
    return render(request, 'store/all_products.html', {
        'products': products,
        'searched': searched,
        'search_query': query
    })

def all_shops(request):
    shops = Shop.objects.all()                                              # SELECT * FROM Shop
    return render(request, 'store/all_shops.html', {'shops': shops})

def update_shop(request):

    shop = Shop.objects.get(id=request.user.shop.id)
    form = ShopForm(instance=shop)


    if request.method == "POST":
        form = ShopForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            form.save()                                                     # UPDATE Shop SET title=form.title, description=form.description... WHERE id=request.user.shop.id

            return redirect('shop', shop_id=request.user.shop.id)

    return render(request, 'store/shop_form.html', {
        'form': form,
        'purpose': 'Update'
    })


    