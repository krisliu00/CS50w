from django.contrib import admin
from .models import AuctionList, Bidding, Comments, WatchList
from core.models import CustomUser

class AuctionListAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'end_time', 'is_active', 'user_id')
    list_filter = ('category', 'end_time', 'is_active')
    search_fields = ('title', 'details') 

class BiddingAdmin(admin.ModelAdmin):
    list_display = ('auction_id', 'bid', 'user_id')
    list_filter = ('auction_id',) 
    search_fields = ('biddings__title', 'bidding_user__username')

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('auction_id', 'comment', 'user_id')
    list_filter = ('auction_id',) 
    search_fields = ('comments__title', 'comment', 'comment_user__username')

class WatchListAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'item_number')
    search_fields = ('watch_list_user__username', 'item_number')

admin.site.register(AuctionList, AuctionListAdmin)
admin.site.register(Bidding, BiddingAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(WatchList, WatchListAdmin)
