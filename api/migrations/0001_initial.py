# Generated by Django 4.2.6 on 2023-10-23 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=100)),
                ('start_time', models.CharField(max_length=50)),
                ('end_time', models.CharField(max_length=50)),
                ('start_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('highest_bid', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('highest_bider', models.CharField(default='', max_length=100)),
            ],
        ),
    ]
