from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Posts
from .util import save_images

def index(request):
    if request.method == "POST":
        text = request.POST.get("text")
        images = request.FILES.getlist("image")
        user = request.user
        post = Posts.objects.create(user=user, text=text)
        post.save()
        if images:
            save_images(images, user, post)

        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/index.html")



