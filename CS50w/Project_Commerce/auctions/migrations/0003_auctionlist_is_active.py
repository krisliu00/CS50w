# Generated by Django 5.0.4 on 2024-05-03 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlist',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
