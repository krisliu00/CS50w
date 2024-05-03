from django.core.management.base import BaseCommand
from django.utils import timezone
from auctions.models import AuctionList

class Command(BaseCommand):
    help = 'Update auction item status based on end time'

    def handle(self, *args, **kwargs):
        expired_items = AuctionList.objects.filter(end_time__lte=timezone.now(), is_active=True)
        for item in expired_items:
            item.is_active = False
            item.save(update_fields=['is_active'])
        self.stdout.write(self.style.SUCCESS('Auction items status updated successfully'))