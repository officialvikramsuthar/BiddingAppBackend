from django.db import models
from UserProfile.models import User


class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    bid_increment = models.DecimalField(max_digits=10, decimal_places=2)
    auction_start = models.DateTimeField()
    auction_end = models.DateTimeField()
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Bid(models.Model):
    item = models.ForeignKey(Item, related_name='bids', on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)