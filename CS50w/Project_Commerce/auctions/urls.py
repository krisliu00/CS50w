from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sell", views.sell, name="sell"),
    path('bidding/<str:item_number>', views.bidding, name="bidding")
    

]