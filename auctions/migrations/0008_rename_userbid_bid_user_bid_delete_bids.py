# Generated by Django 4.2 on 2023-04-07 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_bids'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='userBid',
            new_name='user_bid',
        ),
        migrations.DeleteModel(
            name='Bids',
        ),
    ]
