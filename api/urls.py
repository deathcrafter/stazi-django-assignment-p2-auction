from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import auction, auction_detail, public_auction, bid

urlpatterns = [
    path("auction", auction),
    path("auction/<int:id>", auction_detail),
    path("available_auctions", public_auction),
    path("bid", bid),
]

urlpatterns = format_suffix_patterns(urlpatterns)
