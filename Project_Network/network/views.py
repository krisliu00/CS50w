import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Posts
from core.models import UserProfile
from .util import save_images, post_images, time_setting
from core.models import CustomUser
from django.core.paginator import Paginator

def get_post_data(post, user_instance):
    username = user_instance.username
    customname = user_instance.custom_name
    createtime = post.create_time
    time = time_setting(createtime)
    likes = post.likes if post.likes is not None else 0
    images_path = post_images(username, post)
    images_filenames = os.listdir(images_path) if images_path else []
    
    return {
        'post': post,
        'imagepath': images_path,
        'username': username,
        'customname': customname,
        'image_filenames': images_filenames,
        'time': time,
        'likes': likes
    }

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

    following_posts_data = []
    if request.user.is_authenticated:
        current_user_profile = get_object_or_404(UserProfile, user=request.user)
        following_users = current_user_profile.following.all()
        
        for following_user_profile in following_users:
            following_user = following_user_profile.user
            post_instances = Posts.objects.filter(user=following_user)

            for post in post_instances:
                following_posts_data.append(get_post_data(post, following_user))

    posts = Posts.objects.all()
    posts_data = []
    for post in posts:
        user_instance = CustomUser.objects.get(id=post.user_id)
        posts_data.append(get_post_data(post, user_instance))

    posts_paginator = Paginator(posts_data, 10) 
    following_posts_paginator = Paginator(following_posts_data, 10)

    posts_page_number = request.GET.get('posts_page')
    following_posts_page_number = request.GET.get('following_posts_page')

    posts_page_obj = posts_paginator.get_page(posts_page_number)
    following_posts_page_obj = following_posts_paginator.get_page(following_posts_page_number)

    return render(request, "network/index.html", {
        'posts_page_obj': posts_page_obj,
        'following_posts_page_obj': following_posts_page_obj
    })




