from django.db import models

class Auction(models.Model):
    pieceName = models.CharField(max_length=255)
    artistName = models.CharField(max_length=255)
    preview = models.ImageField(upload_to="previews/")
    condition = models.CharField(max_length=255, default="Minimal Damage")
    description = models.CharField(max_length=1023, default="No Description")

    priceBIN = models.DecimalField(max_digits=13, decimal_places=2, default=0.00)
    startingBid = models.DecimalField(max_digits=13, decimal_places=2, default=0.00)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
           return self.pieceName

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=13, decimal_places=2)
    placedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.amount} on {self.auction.name}"