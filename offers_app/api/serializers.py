from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from django.db.models import Min


class OfferDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type', 'url']
        extra_kwargs = {
            'url': {'view_name': 'offer-detail-view', 'lookup_field': 'pk'}
        }


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    details = OfferDetailSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(source='creator', read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'updated_at',
            'details', 'min_price', 'min_delivery_time', 'url'
        ]
        extra_kwargs = {
            'url': {'view_name': 'offer-detail', 'lookup_field': 'pk'}
        }

    def get_min_price(self, obj):
        return obj.details.aggregate(min_price=Min('price'))['min_price']

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(min_delivery=Min('delivery_time_in_days'))['min_delivery']
