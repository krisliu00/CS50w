from django.shortcuts import render
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from .models import CustomUser, UserProfile
from network.models import Posts
from django.contrib.auth import authenticate
from network.util import save_profile_photo
from django.db.models import Count


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

def UserProfile_view(request, username):

    current_user = request.user
    profile_user = CustomUser.objects.get(username=username)
    profile_user_instances = Posts.objects.filter(user_id=profile_user.id)

    try:
        user_profile = UserProfile.objects.get(user_id=profile_user.id)

    except UserProfile.DoesNotExist:
        following_count = 0
        follower_count = 0

    else:
        following_count = user_profile.following.count()
        follower_count = user_profile.follower.count()
        
        
    return render(request, "core/userprofile.html", {
        'current_user': current_user,
        'profile_user': profile_user,
        'profile_user_instances': profile_user_instances,
        'following_count': following_count,
        'follower_count': follower_count
    })

def setting_profile_view(request):

    if request.method == "POST":
        image = request.FILES.getlist("profile_photo")
        user = request.user
        if image:
            save_profile_photo(image, user)
        
        return render(request, "core/userprofile.html")
    
    else:
        return render(request, "core/setting_profile.html")



