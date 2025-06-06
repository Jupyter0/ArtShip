from django.contrib import admin
from .models import Auction
from .models import Bid

# Register your models here.

admin.site.register(Auction)
admin.site.register(Bid)