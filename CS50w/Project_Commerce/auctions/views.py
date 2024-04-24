from django.shortcuts import redirect, render
from .models import ItemPictures
from .forms import SellList


# Create your views here.

def index(request):
    return render(request, "auctions/index.html")


def sell(request):
    if request.method == "POST":
        form = SellList(request.POST, request.FILES)

        if form.is_valid():
            
            auction_list_instance = form.save()

            images = request.FILES.getlist('image')
            for image in images:
                
                ItemPictures.objects.create(auction_list=auction_list_instance, item_picture=image)

            
            return redirect('success_url')
    else:
        form = SellList()
    return render(request, 'auctions/sell.html', {'form': form})
             

