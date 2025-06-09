from django.utils import timezone
from .models import Auction

def task_runner():
    from auction.tasks import finalize_expired_auctions
    return finalize_expired_auctions()


def finalize_expired_auctions():
    now = timezone.now()
    expired = Auction.objects.filter(
        is_active=True,
        end_time__lte=now
    )

    for auction in expired:
        highest_bid = auction.bids.order_by('-amount').first()
        if highest_bid:
            auction.sold_for = highest_bid.amount
            auction.winner = highest_bid.user
            auction.purchased_by = highest_bid.user
        auction.is_active = False
        auction.save()

    return f"Finalized {expired.count()} expired auctions"
