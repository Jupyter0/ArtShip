from django.urls import path
from . import views as AuctionViews
urlpatterns = [
    path('', AuctionViews.auction, name='auction'),
    path('create/', AuctionViews.create_auction, name='create_auction'),
    path('<slug:slug>/edit/', AuctionViews.edit_auction, name='edit_auction'),
    path('<slug:slug>/', AuctionViews.auction_detail, name="auction_detail"),
]