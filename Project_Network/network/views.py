import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Posts
from core.models import UserProfile
from .util import time_setting
from core.models import CustomUser
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

def get_post_data(post, user_instance, request_user):
    username = user_instance.username
    customname = user_instance.custom_name
    createtime = post.create_time
    time = time_setting(createtime)
    likes = post.likes if post.likes is not None else 0
    is_creator = post.is_creator(request_user)
    id = post.id

    return {
        'post': post,
        'username': username,
        'customname': customname,
        'time': time,
        'likes': likes,
        'id': id,
        'is_creator': is_creator
    }

def index(request):

    if request.method == "POST":
        text = request.POST.get("text")
        user = request.user
        post = Posts.objects.create(user=user, text=text)
        post.save()
    else:
        pass

    following_posts_data = []
    following_posts_page_obj = None
    
    if request.user.is_authenticated:
        current_user_profile = get_object_or_404(UserProfile, user=request.user)
        following_users = current_user_profile.following.all()

        if following_users:
            for following_user_profile in following_users:
                following_user = following_user_profile.user
                post_instances = Posts.objects.filter(user=following_user)

                for post in post_instances:
                    following_posts_data.append(get_post_data(post, following_user, request.user))

            following_posts_paginator = Paginator(following_posts_data, 10)
            following_posts_page_number = request.GET.get('following_posts_page')
            following_posts_page_obj = following_posts_paginator.get_page(following_posts_page_number)

    posts = Posts.objects.all()
    posts_data = []
    for post in posts:
        user_instance = CustomUser.objects.get(id=post.user_id)
        posts_data.append(get_post_data(post, user_instance, request.user))

    posts_paginator = Paginator(posts_data, 10) 
    posts_page_number = request.GET.get('posts_page')
    posts_page_obj = posts_paginator.get_page(posts_page_number)
    
    
    return render(request, "network/index.html", {
        'posts_page_obj': posts_page_obj,
        'following_posts_page_obj': following_posts_page_obj,
    })


@require_http_methods(["POST"])
@login_required
def likes_api(request, post_id):

    try:
        post = Posts.objects.get(id=post_id)
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'like':
            post.likes = (post.likes or 0) + 1
        elif action == 'unlike' and post.likes > 0:
            post.likes -= 1
        
        post.save()
        return JsonResponse({"success": True, "likes": post.likes})
    except Posts.DoesNotExist:
        return JsonResponse({"success": False, "error": "Post not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@login_required
def edit_post_api(request, post_id):
    try:
        post = Posts.objects.get(id=post_id)
        if not post.is_creator(request.user):
            return JsonResponse({"success": False, "error": "You do not have permission to edit this post"}, status=403)
        
        data = json.loads(request.body)
        post.text = data.get('text', post.text)
        post.save()
        return JsonResponse({"success": True, "text": post.text})
    except Posts.DoesNotExist:
        return JsonResponse({"success": False, "error": "Post not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)