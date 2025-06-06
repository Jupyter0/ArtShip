from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from .models import Auction

def auction(request):
    auctions = Auction.objects.all()

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        auctions = auctions.filter(priceBIN__gte=min_price)
    if max_price:
        auctions = auctions.filter(priceBIN__lte=max_price)
    if min_price and max_price:
        auctions = auctions.filter(priceBIN__range=(min_price, max_price))
    
    return HttpResponse(render(request, 'auction/auction.html', {'auctions' : auctions}))

def auction_detail(request, slug):
    auction = get_object_or_404(Auction, slug=slug)
    highest_bid = auction.bids.order_by('-amount').first()
    bid_history = auction.bids.order_by('-placedAt')
    return render(request, 'auction/detail.html', {
        'auction': auction,
        'highest_bid': highest_bid,
        'bid_history': bid_history,
    })