# Generated by Django 5.0.4 on 2024-05-17 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_posts_delete_post'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posts',
            options={'verbose_name_plural': 'Posts'},
        ),
        migrations.AlterField(
            model_name='posts',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]