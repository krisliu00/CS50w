import os
import uuid
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from .models import AuctionList
from .forms import SellList, BiddingForm
from .util import save_images, current_price
from datetime import timedelta
from django.utils import timezone


# Create your views here.

def index(request):
    return render(request, "auctions/index.html")


def sell(request):
    if request.method == "POST":
        form = SellList(request.POST, request.FILES)

        if form.is_valid():

            auction_list_instance = form.save(commit=False)
            item_number = uuid.uuid4().hex[:10]
            auction_list_instance.item_number = item_number
            expiration_time = timezone.now() + timedelta(days=2)
            auction_list_instance.end_time = expiration_time
            auction_list_instance.save()

            images = request.FILES.getlist('images')
            save_images(images, item_number)
        
            return redirect('bidding', item_number=item_number)
    
    else:
        form = SellList()
    return render(request, 'auctions/sell.html', {'form': form})

def bidding(request, item_number):
    auction_instance = get_object_or_404(AuctionList, item_number=item_number)

    if request.method == "POST":
        bidform = BiddingForm(request.POST)
        if bidform.is_valid():
            bidding_instance = bidform.save(commit=False)
            bidding_instance.auction = auction_instance
            bidding_instance.save()
            return redirect('bidding', item_number=item_number)
        if not bidform.is_valid():
            return render(request, 'auctions/bidding.html', {
        
        'item_number': item_number, 

        'bidform': bidform
    })
    else:
        bidform=BiddingForm()
    
    auctions = AuctionList.objects.filter(item_number=item_number)
    folder_path = os.path.join(settings.MEDIA_ROOT, 'items', str(item_number))
    image_filenames = os.listdir(folder_path)
    bidform = BiddingForm()
    print(bidform.errors)
    

    return render(request, 'auctions/bidding.html', {
        'auctions': auctions, 
        'item_number':item_number, 
        'images':image_filenames, 
        'bidform' :bidform}) 
             

