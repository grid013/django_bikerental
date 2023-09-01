from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from accounts.forms import LoginForm, RegisterForm

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            print(user)
            auth.login(request, user)
            return redirect('/')
        else:
            print("here")
            messages.info(
                request, 'Invalid!!, Check your username or password.')
            return redirect('/')
    else:
        form=LoginForm()
        return render(request, 'login.html', {"form":form})


def logout(request):
    auth.logout(request)
    messages.info(
                request, 'You are logged out.')
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, "Your account has been created! Your are now able to login.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form":form})