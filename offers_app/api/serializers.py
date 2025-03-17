from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from django.db.models import Min


class OfferDetailSerializer(serializers.ModelSerializer):
    """ Serializer für ein einzelnes OfferDetail """
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type']


class OfferSerializer(serializers.ModelSerializer):
    """ Serializer für ein Angebot mit OfferDetails """
    details = OfferDetailSerializer(
        many=True)  # Setze read_only=False, um Updates zu erlauben
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(source='creator', read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'updated_at',
            'details', 'min_price', 'min_delivery_time'
        ]

    def get_min_price(self, obj):
        return obj.details.aggregate(min_price=Min('price'))['min_price']

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(min_delivery=Min('delivery_time_in_days'))['min_delivery']

    def update(self, instance, validated_data):
        """ Ermöglicht das Aktualisieren von verschachtelten `details` """
        details_data = validated_data.pop(
            'details', None)  # `details` extrahieren, falls vorhanden

        # Aktualisiere die Offer-Daten (z.B. Titel, Beschreibung, etc.)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Falls `details` mitgegeben wurden, aktualisiere sie:
        if details_data is not None:
            instance.details.all().delete()  # Lösche existierende Details
            for detail_data in details_data:
                OfferDetail.objects.create(
                    offer=instance, **detail_data)  # Neue erstellen

        return instance
