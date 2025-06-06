from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from .models import Auction
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

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
    
    for auction in auctions:
        auction.highestBid = auction.bids.order_by('-amount').first()
    
    return HttpResponse(render(request, 'auction/auction.html', {'auctions' : auctions}))

def auction_detail(request, slug):
    auction = get_object_or_404(Auction, slug=slug)
    highest_bid = auction.bids.order_by('-amount').first()
    bid_history = auction.bids.order_by('-placedAt')

    if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to bid or buy.")
            return redirect('login')

    if request.method == "POST" and auction.is_active:
        action = request.POST.get('action')

        if action == "buy":
            auction.is_active = False
            auction.save()
            messages.success(request, "You have successfully bought this item.")
            return redirect('auction_detail', slug=auction.slug)

        elif action == "bid":
            bid_amount = request.POST.get('bid_amount')
            if bid_amount:
                bid_amount = float(bid_amount)

                min_bid = highest_bid.amount + 1 if highest_bid else auction.startingBid

                if bid_amount >= min_bid:
                    from .models import Bid
                    Bid.objects.create(
                        auction=auction,
                        user=request.user,
                        amount=bid_amount
                    )
                    messages.success(request, "Your bid has been placed.")
                    return redirect('auction_detail', slug=auction.slug)
                else:
                    messages.error(request, f"Your bid must be at least US ${round(min_bid, 2):,}.")

    return render(request, 'auction/detail.html', {
        'auction': auction,
        'highest_bid': highest_bid,
        'bid_history': bid_history,
    })