from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

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
            return redirect('home')
        else:
            # Login error message
            messages.success(request, ('Error loging in !!!'))
            return redirect('login')
    
    # Landing page
    else:
        return render(request, 'member/login.html', {})
    
def logout_member(request):
    logout(request)
    messages.success(request, 'You were logged out')
    return redirect('home')