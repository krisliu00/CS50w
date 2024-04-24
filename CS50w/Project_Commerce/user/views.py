from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import UserRegistrationForm, UserLoginForm


# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            login(request, user)  
            return HttpResponseRedirect(reverse("auctions:index"))
    else:
        form = UserRegistrationForm()
    return render(request, "user/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":

        Loginform = UserLoginForm(request.POST)

        if Loginform.is_valid():
            username = Loginform.cleaned_data['username']
            password = Loginform.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("auctions:index"))
            else:
                return render(request, "user/login.html", {
                    "form": Loginform,
                    "message": "Invalid username and/or password."
                })
            
    else:
        Loginform = UserLoginForm()
    return render(request, "user/login.html", {"form": Loginform})