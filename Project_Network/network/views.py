import os
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Posts
from .util import save_images, post_images, time_setting
from core.models import CustomUser

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
        pass

    posts = Posts.objects.all()
    posts_data = []
    for post in posts:
        user_instance = CustomUser.objects.get(id=post.user_id)
        username = user_instance.username
        customname = user_instance.custom_name
        createtime = post.create_time
        time = time_setting(createtime)
        likes = post.likes


        images_path = post_images(username, post)
        images_filenames = [] 
        if images_path is not None:

            images_filenames = os.listdir(images_path)

        posts_data.append({
            'post': post,
            'imagepath': images_path,
            'username': username,
            'customname': customname,
            'image_filenames': images_filenames,
            'time': time
        })

    return render(request, "network/index.html", {'posts_data': posts_data})




