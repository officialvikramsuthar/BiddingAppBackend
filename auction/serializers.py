from django.utils import timezone
from rest_framework import serializers
from .models import Item, Bid


class ItemSerializer(serializers.ModelSerializer):
    auction_start = serializers.DateTimeField(format="%Y-%m-%d")
    auction_end = serializers.DateTimeField(format="%Y-%m-%d")
    highest_bid = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'title', 'description', 'starting_bid', 'bid_increment', 'auction_start', 'auction_end', 'image', 'highest_bid']

    def get_highest_bid(self, obj):
        highest_bid = Bid.objects.filter(item=obj).order_by('-amount').first()
        return highest_bid.amount if highest_bid else 0


class BidSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", default=timezone.now())

    class Meta:
        model = Bid
        fields = ['id', 'item', 'amount', 'timestamp']