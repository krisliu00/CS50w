import os
import uuid
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from .models import AuctionList,Comments, Bidding, WatchList
from .forms import SellList, BiddingForm, CommentForm
from .util import save_images, index_image, highest_bidding, watchlist_image, close_list
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# Create your views here.

def index(request):
    instances = AuctionList.objects.filter(is_active=True)

    active_list = [(index_image(instance.item_number), instance.item_number) for instance in instances]
    
    user = request.user if request.user.is_authenticated else None
    
    return render(request, "auctions/index.html", {
        'active_list': active_list,
        'user': user
    })



def sell(request):
    if request.method == "POST":
        form = SellList(request.POST, request.FILES)

        if form.is_valid():
            if request.user.is_authenticated:

                auction_list_instance = form.save(commit=False)
                item_number = uuid.uuid4().hex[:10]
                auction_list_instance.item_number = item_number
                expiration_time = datetime.now() + timedelta(days=2)
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
    current_price = highest_bidding(auction_instance.item_number)
    starting_price = auction_instance.price
    item_in_watchlist = False
    if request.method == "POST":
        if request.user.is_authenticated:
            if 'bid' in request.POST:
                bidform = BiddingForm(request.POST)

                if bidform.is_valid():
                    bid_value = bidform.cleaned_data.get('bid')
                    if (current_price is None and bid_value > starting_price) or (current_price is not None and bid_value > current_price):
                        bidding_instance = bidform.save(commit=False)
                        if bidding_instance is not None:
                            bidding_instance.auction = auction_instance
                            bidding_instance.user = request.user
                            bidding_instance.save()
                            return redirect('auctions:bidding', item_number=item_number)
                    else:
                        messages.error(request, 'Invalid bid value.')

            elif 'comment' in request.POST:
                commentform = CommentForm(request.POST)
                if commentform.is_valid():
                    comment_instance = commentform.save(commit=False)
                    if comment_instance is not None: 
                        comment_instance.auction = auction_instance
                        comment_instance.user = request.user
                        comment_instance.save()
                        return render('auctions:bidding', item_number=item_number)
    else:
        pass
    
    comments = Comments.objects.filter(auction=auction_instance)
    biddings = Bidding.objects.filter(auction=auction_instance)
    folder_path = os.path.join(settings.MEDIA_ROOT, 'items', str(item_number))
    image_filenames = os.listdir(folder_path)

    if request.user.is_authenticated:
        item_in_watchlist = WatchList.objects.filter(user=request.user, item_number=item_number).exists()
        
    return render(request, 'auctions/bidding.html', {
        'auction': auction_instance,
        'item_number':item_number, 
        'images':image_filenames, 
        'bidform' :bidform,
        'commentform': commentform,
        'comments': comments,
        'biddings':biddings,
        'current_price':current_price,        
        'item_in_watchlist': item_in_watchlist,
        'request': request
        }) 

@login_required
def watchlist(request):
    item_number = request.POST.get('item_number') 
    current_user = request.user

    if request.method == "POST":
        
        if not WatchList.objects.filter(user=request.user, item_number=item_number).exists():
                
            WatchList.objects.create(user=request.user, item_number=item_number)
            return redirect('auctions:bidding', item_number=item_number)

        else:
            WatchList.objects.filter(user=request.user, item_number=item_number).delete()
            return redirect('auctions:bidding', item_number=item_number)
        
    else:        
            file_paths = []
            watchlist_instances = WatchList.objects.filter(user=current_user)
            for obj in watchlist_instances:
                file_path = watchlist_image(obj.item_number)
                file_paths.append(file_path)
    
    return render(request, 'auctions/watchlist.html',{
        'watchlist_images': file_paths,
    })

@login_required
def Closelist(request):
    if request.method == "POST":
        user_id = request.user.id
        form_item_number = request.POST.get('item_number')
        close_list(user_id, form_item_number)
        return redirect('auctions:bidding', item_number=form_item_number)
