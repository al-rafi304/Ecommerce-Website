from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm
from store.models import Cart

# Create your views here.
def login_member(request):
    # If form has been submitted
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Catching erros
        if user is not None:
            login(request, user)
            messages.success(request, f'You are now logged in as {request.user.username}')
            return redirect('home')
        else:
            # Login error message
            messages.error(request, ('Error loging in !!!'))
            return redirect('login')
    
    # Landing page
    else:
        return render(request, 'member/login.html', {})
    
def logout_member(request):
    logout(request)
    messages.warning(request, 'You were logged out')
    return redirect('home')

def register_member(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            cart_obj = Cart.objects.create(member=user)
            messages.success(request, f'You are now logged in as {request.user.username}')
            return redirect('home')
        else:
            print(form.error_messages)
    else:
        form = RegisterForm()
    return render(request, 'member/register.html', {'form': form})