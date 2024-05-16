from django.shortcuts import render
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from .models import CustomUser
from django.contrib.auth import authenticate


# Create your views here.
def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        custom_name = request.POST["customname"]
        bio = request.POST["bio"]
        age = request.POST["age"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "core/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = CustomUser.objects.create_user(username=username, email=email, custom_name=custom_name, bio=bio, age=age, password=password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "core/register.html", {
                "message": "Username or email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "core/register.html")

def login_view(request):
    if request.method == "POST":

        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "core/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "core/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))
