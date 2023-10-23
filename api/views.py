from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import *

import jwt

# Create your views here.


@api_view(["GET", "POST"])
def auction(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    if auth_header is None:
        return Response(status=401)

    token = auth_header.split(" ")[1]
    if token != "admin-secret-token":
        return Response(status=401)

    if request.method == "GET":
        auctions = Auction.objects.all()
        serializer = AuctionSerializer(auctions, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CreateAuctionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(["GET", "PUT", "DELETE"])
def auction_detail(request, id):
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    if auth_header is None:
        return Response(status=401)

    token = auth_header.split(" ")[1]
    if token != "admin-secret-token":
        return Response(status=401)

    auction = Auction.objects.filter(id=id)

    if not auction.exists():
        return Response(status=404)

    if request.method == "GET":
        serializer = AuctionSerializer(auction.get())
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CreateAuctionSerializer(
            auction.get(), data=request.data, partial=True
        )
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == "DELETE":
        auction.delete()
        return Response(status=204)


@api_view(["GET"])
def public_auction(_request):
    now = datetime.now().isoformat()

    auctions = Auction.objects.filter(
        start_time__lte=now,
        end_time__gte=now,
    )
    serializer = PublicAuctionSerializer(auctions, many=True)
    data = serializer.data

    return Response(data)
    # live_auctions = list()
    # for auction in data:
    #     if auction["start_time"] < now and auction["end_time"] > now:
    #         live_auctions.append(auction)

    # serializer = PublicAuctionSerializer(data=live_auctions, many=True)
    # if serializer.is_valid():
    #     return Response(serializer.data)
    # return Response(serializer.errors)


@api_view(["POST"])
def bid(request):
    authheader = request.META.get("HTTP_AUTHORIZATION")
    if authheader is None:
        return Response(status=401)

    token = authheader.split(" ")[1]
    payload = jwt.decode(token, "secret", algorithms=["HS256"])

    user = payload["email"]
    bid_amount = float(request.data["bid_amount"])

    try:
        auction = Auction.objects.get(id=request.data["auction_id"])
    except Auction.DoesNotExist:
        return Response({"error": "Auction does not exist"}, status=404)

    if auction.end_time < datetime.now().isoformat():
        return Response({"error": "Auction has ended"}, status=403)

    if auction.highest_bid > bid_amount:
        return Response(
            {
                "error": "Bid must be higher than current bid {amount}".format(
                    amount=auction.highest_bid
                ),
            },
            status=400,
        )

    serializer = AuctionSerializer(
        auction, data={"highest_bid": bid_amount, "highest_bider": user}, partial=True
    )
    if serializer.is_valid():
        serializer.save()
        return Response(status=200)

    return Response(serializer.errors, status=400)
