# Generated by Django 4.2 on 2023-04-05 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_lot_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='category',
            field=models.CharField(default='', max_length=64),
        ),
    ]