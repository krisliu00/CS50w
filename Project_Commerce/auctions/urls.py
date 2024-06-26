from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'auctions'

urlpatterns = [
    path("", views.index, name="index"),
    path("sell", views.sell, name="sell"),
    path('bidding/<str:item_number>', views.bidding, name="bidding"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('closelist', views.Closelist, name="closelist"),
    path('myauction', views.MyAuctionView, name="myauction"),
    path('category', views.CategoryView, name="category"),
    path('<str:category>/', views.SublistView, name="sublist")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)