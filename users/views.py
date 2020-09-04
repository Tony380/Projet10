from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView


def register(request):
    """ User registration function """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            messages.success(request,
                             'Bienvenu! Votre compte a été créé avec succès! '
                             'Vous êtes maintenant connecté')
            login(request, user)
            return redirect('index')
        else:
            form = RegisterForm(request.POST)
            return render(request, 'register.html', {'form': form})

    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    """ User's profile page """
    return render(request, 'profile.html')


class LoginFormView(SuccessMessageMixin, LoginView):
    """ Add a welcome message when user logs in """
    success_message = "Bienvenu! Vous êtes maintenant connecté"


@login_required
def logout_view(request):
    """ User logout function """
    logout(request)
    messages.success(request, 'Au revoir! Vous êtes maintenant déconnecté')
    return redirect('index')
