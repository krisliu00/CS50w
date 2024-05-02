import os
import uuid
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from .models import AuctionList,Comments
from .forms import SellList, BiddingForm, CommentForm
from .util import save_images, index_image
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user = request.user

    instances = AuctionList.objects.filter(end_time__gt=timezone.now())
    active_list = []

    for instance in instances:
        image_path = index_image(instance.item_number)
        item_number = instance.item_number
        instance_tuple = (image_path, item_number)
        active_list.append(instance_tuple)

    return render(request, "auctions/index.html", {
        'active_list': active_list,
        'user' : user
        })



def sell(request):
    if request.method == "POST":
        form = SellList(request.POST, request.FILES)

        if form.is_valid():
            if request.user.is_authenticated:

                auction_list_instance = form.save(commit=False)
                item_number = uuid.uuid4().hex[:10]
                auction_list_instance.item_number = item_number
                expiration_time = timezone.now() + timedelta(days=2)
                auction_list_instance.end_time = expiration_time
                auction_list_instance.user = request.user
                auction_list_instance.save()

                images = request.FILES.getlist('images')
                save_images(images, item_number)
            
                return redirect('auctions:bidding', item_number=item_number)
    
    else:
        form = SellList()
    return render(request, 'auctions/sell.html', {'form': form})

def bidding(request, item_number):
    auction_instance = get_object_or_404(AuctionList, item_number=item_number)
    bidform=BiddingForm()
    commentform = CommentForm()

    if request.method == "POST":
        if request.user.is_authenticated:
            if 'bid' in request.POST:
                bidform = BiddingForm(request.POST)
                if bidform.is_valid():
                    bidding_instance = bidform.save(commit=False)
                    if bidding_instance is not None:
                        bidding_instance.auction = auction_instance
                        comment_instance.user = request.user
                        bidding_instance.save()
                        return redirect('auctions:bidding', item_number=item_number)
            
            elif 'comment' in request.POST:
                commentform = CommentForm(request.POST)
                if commentform.is_valid():
                    comment_instance = commentform.save(commit=False)
                    if comment_instance is not None: 
                        comment_instance.auction = auction_instance
                        comment_instance.user = request.user
                        comment_instance.save()
                        return redirect('auctions:bidding', item_number=item_number)
    else:
        pass
    
    comments = Comments.objects.filter(auction=auction_instance)
    folder_path = os.path.join(settings.MEDIA_ROOT, 'items', str(item_number))
    image_filenames = os.listdir(folder_path)
    
    return render(request, 'auctions/bidding.html', {
        'auction': auction_instance,
        'item_number':item_number, 
        'images':image_filenames, 
        'bidform' :bidform,
        'commentform': commentform,
        'comments': comments
        }) 