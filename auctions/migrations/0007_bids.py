# Generated by Django 4.2 on 2023-04-07 05:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_lot_description_alter_lot_lot_bid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_bid', models.DecimalField(decimal_places=2, max_digits=7)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.lot')),
            ],
        ),
    ]