import uuid
from django.shortcuts import redirect, render
from .models import AuctionList
from .forms import SellList
from .util import save_images
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

    auctions = AuctionList.objects.filter(item_number=item_number)

    return render(request, 'auctions/bidding.html', {'auctions': auctions}) 
             

