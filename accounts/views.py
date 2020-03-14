from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegisterForm
from main.utils import send_email


def login_view(request):

    if request.user.is_authenticated:
        return redirect(reverse('index'))

    # Checking if user was redirected to login page
    # and getting the url they were trying to access.
    next = request.GET.get('next')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)

                if remember_me:
                    request.session.set_expiry(30)

                if next:
                    return redirect(next)
                else:
                    return redirect(reverse('index'))

    else:
        form = UserLoginForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/login.html', context=context)


def register_view(request):

    if request.user.is_authenticated:
        return redirect(reverse('index'))

    next = request.GET.get('next')

    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")

        user = form.save(commit=False)
        user.set_password(password)
        user.save()

        subject = "Thank you for registering to NISQ Algorithm Zoo"
        message ="You can now login as {} and submit new NISQ algorithm implementations.".format(username)
        send_email(subject, email, message)

        new_user = authenticate(username=username, password=password)

        if new_user:
            login(request, new_user)

            if next:
                return redirect(next)
            else:
                return redirect(reverse('index'))

    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context=context)


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))



        
        
        