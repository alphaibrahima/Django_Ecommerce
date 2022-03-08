from imaplib import _Authenticator
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from .forms import RegistrationForm
from .models import Account

# Create your views here.


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            # on cree un nom d'utilisateur de lemail et le diviser en deux l'avant @ et lapres 
            # on prend le premier 
            username = email.split('@')[0]
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
    else:
        form = RegistrationForm() 
    context = {
        'form' : form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print(email)

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            # User is authenticated
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'les information n\'est valide')
            return redirect ('login')
    return render(request, 'accounts/login.html')