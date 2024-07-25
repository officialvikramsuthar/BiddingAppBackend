from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.mail import send_mail
from django.db.models import Max
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from .models import Item, Bid
from .serializers import ItemSerializer, BidSerializer
from rest_framework import viewsets


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    permission_classes = [IsAuthenticated|ReadOnly]
    serializer_class = ItemSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated|ReadOnly]

    def perform_create(self, serializer):
        serializer.save(bidder=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        item_id = response.data.get('item')
        amount = response.data.get('amount')

        if item_id:
            item_bids = Bid.objects.aggregate(max_amount=Max('amount', default=0))
            item = Item.objects.filter(id=item_id).first()

            if item_bids and amount >= item_bids['max_amount']:
                highest_bid = item_bids[1]
                # send_mail(
                #     'Outbid Notification',
                #     f'You have been outbid on item {item.title}.',
                #     'from@example.com',
                #     [highest_bid.bidder.email or highest_bid.bidder.mobile_number]
                # )

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "items",
                {
                    "type": "item.update",
                    "item": ItemSerializer(item).data
                }
            )
        return response

