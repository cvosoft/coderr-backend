from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from django.db.models import Min


# Kein HyperlinkedModelSerializer!
class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type']


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)  # 🔥 Details jetzt schreibbar
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(source='creator', read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'updated_at',
            'details', 'min_price', 'min_delivery_time'
        ]

    def create(self, validated_data):
        """ Erstellt ein Angebot mit OfferDetails """
        details_data = validated_data.pop(
            'details', [])  # Details aus JSON extrahieren
        offer = Offer.objects.create(**validated_data)  # Angebot speichern

        # 🔥 Jetzt die Details speichern
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer

    def get_min_price(self, obj):
        return obj.details.aggregate(min_price=Min('price'))['min_price']

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(min_delivery=Min('delivery_time_in_days'))['min_delivery']
