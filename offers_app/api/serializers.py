from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from django.db.models import Min


class OfferDetailURLSerializer(serializers.ModelSerializer):
    """ Gibt ID und URL des Details zurück. """

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class UserDetailsSerializer(serializers.Serializer):
    """ Gibt User-Daten aus. """
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailURLSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'title', 'image', 'description', 'updated_at',
            'details', 'min_price', 'min_delivery_time', 'user_details'
        ]

    def get_min_price(self, obj):
        """ Berechnet den minimalen Preis eines Angebots. """
        return obj.details.aggregate(min_price=Min('price'))['min_price']

    def get_min_delivery_time(self, obj):
        """ Berechnet die minimale Lieferzeit eines Angebots. """
        return obj.details.aggregate(min_delivery=Min('delivery_time_in_days'))['min_delivery']

    def get_user_details(self, obj):
        """ Holt User-Details """
        return {
            "first_name": obj.creator.first_name,
            "last_name": obj.creator.last_name,
            "username": obj.creator.username
        }
