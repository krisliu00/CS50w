from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'auctions'

urlpatterns = [
    path("", views.index, name="index"),
    path("sell", views.sell, name="sell"),
    path('bidding/<str:item_number>', views.bidding, name="bidding")
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)