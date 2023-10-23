from rest_framework.serializers import ModelSerializer, Serializer
from api.models import Auction, models
from datetime import datetime


def toIso(dt: str):
    return datetime.fromisoformat(dt)


class AuctionSerializer(ModelSerializer):
    class Meta:
        model = Auction
        fields = (
            "id",
            "item_name",
            "start_time",
            "end_time",
            "start_price",
            "highest_bid",
            "highest_bider",
        )


class PublicAuctionSerializer(ModelSerializer):
    class Meta:
        model = Auction
        fields = (
            "id",
            "item_name",
            "start_time",
            "end_time",
            "start_price",
            "highest_bid",
        )


class CreateAuctionSerializer(ModelSerializer):
    class Meta:
        model = Auction
        fields = ("item_name", "start_time", "end_time", "start_price")

    def verify(self, data):
        if datetime.fromisoformat(data["start_time"]) < datetime.now():
            raise Serializer.ValidationError(
                "Start time must be in the future",
            )
        if data["start_time"] <= data["end_time"]:
            raise Serializer.ValidationError(
                "Start time must be before end time",
            )
        return super().verify(data)


class UpdateAuctionSerializer(Serializer):
    item_name = models.CharField(max_length=100)
    start_time = models.CharField(max_length=50)
    end_time = models.CharField(max_length=50)
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
