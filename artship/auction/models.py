from django.db import models
from django.utils.text import slugify

class Auction(models.Model):
    pieceName = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, unique=True)
    artistName = models.CharField(max_length=255)
    preview = models.ImageField(upload_to="previews/")
    condition = models.CharField(max_length=255, default="Minimal Damage")
    description = models.CharField(max_length=1023, default="No Description")

    priceBIN = models.DecimalField(max_digits=13, decimal_places=2, default=0.00)
    startingBid = models.DecimalField(max_digits=13, decimal_places=2, default=0.00)
    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.pieceName)
            slug = base_slug
            counter = 1
            while Auction.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
           return self.pieceName

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=13, decimal_places=2)
    placedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.amount} on {self.auction.name}"