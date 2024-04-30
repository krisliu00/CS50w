from django.contrib import admin
from .models import AuctionList, Bidding, Comments

class AuctionListAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'end_time', 'item_number')
    list_filter = ('category', 'end_time')
    search_fields = ('title', 'item_number')
    date_hierarchy = 'end_time'
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        queryset.delete()
    delete_selected.short_description = "Delete selected items"

class BiddingAdmin(admin.ModelAdmin):
    list_display = ('auction', 'bid')
    search_fields = ('auction__title', 'bid')

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('auction', 'comment')
    search_fields = ('auction__title', 'comment')

admin.site.register(AuctionList, AuctionListAdmin)
admin.site.register(Bidding, BiddingAdmin)
admin.site.register(Comments, CommentsAdmin)
