from django.shortcuts import render
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import UserRegistrationForm,UserLoginForm
from .models import CustomUser
from django.contrib.auth import authenticate


# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = CustomUser.objects.create_user(
                username=cleaned_data['username'],
                email=cleaned_data['email'],
                password=cleaned_data['password'],
                custom_name=cleaned_data['custom_name'],
                age=cleaned_data['age'],
                bio=cleaned_data['bio']
            ) 
            login(request, user)  
            return HttpResponseRedirect(reverse("network:index"))
    else:
        form = UserRegistrationForm()
    return render(request, "core/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":

        Loginform = UserLoginForm(request.POST)

        if Loginform.is_valid():
            username = Loginform.cleaned_data['username']
            password = Loginform.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('network:index'))
            else:
                return render(request, "core/login.html", {
                    "form": Loginform,
                    "message": "Invalid username and/or password."
                })
            
    else:
        Loginform = UserLoginForm()
    return render(request, "core/login.html", {"form": Loginform})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))
