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
    bidding_status = highest_bidding(auction_instance.item_number)
    highest_bid = None
    winner = None
    if bidding_status is not None:
        highest_bid = bidding_status[0]
        winner = bidding_status[1]
    bidform=BiddingForm()
    commentform = CommentForm()
    starting_price = auction_instance.price
    item_in_watchlist = False
    if request.method == "POST":
        if request.user.is_authenticated:
            if 'bid' in request.POST:
                bidform = BiddingForm(request.POST)

                if bidform.is_valid():
                    bid_value = bidform.cleaned_data.get('bid')
                    if (highest_bid is None and bid_value > starting_price) or (highest_bid is not None and bid_value > highest_bid):
                        bidding_instance = bidform.save(commit=False)
                        if bidding_instance is not None:
                            bidding_instance.auction = auction_instance
                            bidding_instance.user = request.user
                            bidding_instance.save()
                            return redirect('auctions:bidding', item_number=auction_instance.item_number)
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
                        return redirect('auctions:bidding', item_number=auction_instance.item_number)
    else:
        pass
    
    comments = Comments.objects.filter(auction=auction_instance)
    biddings = Bidding.objects.filter(auction=auction_instance)
    folder_path = os.path.join(settings.MEDIA_ROOT, 'items', str(item_number))
    image_filenames = os.listdir(folder_path)
    is_creator = auction_instance.is_creator(request.user)
   
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
        'item_in_watchlist': item_in_watchlist,
        'request': request,
        'highest_bid': highest_bid,
        'winner': winner,
        'is_creator': is_creator
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
            watchlist_instances = WatchList.objects.filter(user=current_user)
            watchlist_item_with_images = [(watchlist_image(obj.item_number), obj.item_number) for obj in watchlist_instances]

    return render(request, 'auctions/watchlist.html',{
        'watchlist_item_with_images': watchlist_item_with_images
    })

@login_required
def Closelist(request):
    if request.method == "POST":
        user_id = request.user.id
        form_item_number = request.POST.get('item_number')
        close_list(user_id, form_item_number)
        return redirect('auctions:bidding', item_number=form_item_number)

@login_required
def MyAuctionView(request):

    my_items = AuctionList.objects.filter(user=request.user).prefetch_related('comments', 'biddings')

    commented_auction_ids = set(Comments.objects.filter(user=request.user).values_list('auction_id', flat=True))

    bidding_auction_ids = set(Bidding.objects.filter(user=request.user).values_list('auction_id', flat=True))

    user_involved_auction_ids = commented_auction_ids.union(bidding_auction_ids)

    user_involved_items = AuctionList.objects.filter(item_number__in=user_involved_auction_ids).prefetch_related('comments', 'biddings')

    closed_bidded_items = AuctionList.objects.filter(item_number__in=bidding_auction_ids, is_active=False).prefetch_related('biddings')
    
    won_items = {}

    for item in closed_bidded_items:

        hightest_bid_amount = highest_bidding(item.item_number)
        user_bid_amount = item.biddings.filter(user=request.user)

        if user_bid_amount[0].bid == hightest_bid_amount[0]:

            won_items[item.item_number] = {'title': item.title, 'bid_amount': user_bid_amount[0].bid}


    myauction_list = [(watchlist_image(item.item_number), item.item_number) for item in my_items]

    comment_mapping = {}
    bidding_mapping = {}

    for item in user_involved_items:
        if item.item_number in commented_auction_ids:
            comments_for_item = item.comments.filter(user=request.user)
            comment_mapping[item.title] = [comment.comment for comment in comments_for_item]
        if item.item_number in bidding_auction_ids:
            bids_for_item = item.biddings.filter(user=request.user)
            bidding_mapping[item.title] = [bid.bid for bid in bids_for_item]

    return render(request, "auctions/myauction.html", {
        'myauction_list': myauction_list,
        'comment_mapping': comment_mapping,
        'bidding_mapping': bidding_mapping,
        'won_items': won_items
    })
# another method for MyAuctionView
#  def MyAuctionView(request):
#     my_items = AuctionList.objects.filter(user=request.user)
#     my_comments = Comments.objects.filter(user=request.user)
#     my_biddings = Bidding.objects.filter(user=request.user)

#     commented_auction_ids = my_comments.values_list('auction_id', flat=True).distinct()
#     bidding_auction_ids = my_biddings.values_list('auction_id', flat=True).distinct()

#     comments_items = AuctionList.objects.filter(item_number__in=commented_auction_ids)
#     bidding_items = AuctionList.objects.filter(item_number__in=bidding_auction_ids)

#     mycomments_titles = list(comments_items.values_list('title', flat=True))
#     mybiddings_titles = list(bidding_items.values_list('title', flat=True))

#     comments = [comment.comment for comment in my_comments]
#     biddings = [bid.bid for bid in my_biddings]

#     items_with_comments = zip(mycomments_titles, comments)
#     item_with_biddings = zip(mybiddings_titles, biddings)
  
#     for obj in my_items:
#         myauction_list = [(watchlist_image(obj.item_number), item.item_number) for item in my_items]
   
#     return render(request, "auctions/myauction.html", {
#         'items_with_comments': items_with_comments,
#         'myauction_list': myauction_list,
#         'item_with_biddings': item_with_biddings
#     })

def CategoryView(request):
    categories = ['fashion', 'electronics', 'accessories', 'toy', 'furniture', 'others']

    category_items = {}
    for category in categories:
        instances = AuctionList.objects.filter(category=category, is_active=True).order_by('category', 'item_number')
        category_items[category] = [{'item_number': instance.item_number, 'category': instance.category, 'image_path': index_image(instance.item_number) } for instance in instances]

    return render(request, "auctions/category.html", {
        'category_items': category_items
    })
        
def SublistView(request, category):
    instances = AuctionList.objects.filter(category=category, is_active=True).order_by('category', 'item_number')
    category_items = {}
    category_items[category] = [{'item_number': instance.item_number, 'image_path': index_image(instance.item_number) } for instance in instances]
    return render(request, "auctions/sublisting.html",{
        'listing_items': category_items,
        'category': category
    })
