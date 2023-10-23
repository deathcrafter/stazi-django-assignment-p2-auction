from django.db import models

# Create your models here.


class Auction(models.Model):
    id = models.AutoField(primary_key=True)

    item_name = models.CharField(max_length=100)

    # store dates in ISO format
    start_time = models.CharField(max_length=50)
    end_time = models.CharField(max_length=50)

    start_price = models.DecimalField(max_digits=10, decimal_places=2)

    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    highest_bider = models.CharField(max_length=100, default="")  # email
