from celery import Celery
from django.conf import settings

app = Celery('auctions')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(24 * 60 * 60, update_auction_status.s(), name='update-auction-status')

@app.task
def update_auction_status():
    from django.core.management import call_command
    call_command('update_auction_status')