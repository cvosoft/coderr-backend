from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from django.db.models import Min
from django.urls import reverse


class OfferDetailSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer für ein einzelnes OfferDetail mit URL-Referenz """
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']  # Gibt nur ID und URL zurück
        extra_kwargs = {
            'url': {'view_name': 'offer-detail-view', 'lookup_field': 'pk'}
        }


class OfferSerializer(serializers.ModelSerializer):
    # details = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='offer-detail-view',
    #     lookup_field='pk'
    # )
    details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(source='creator', read_only=True)

    # Hier das gewünschte Datumsformat definieren (ohne Mikrosekunden)
    created_at = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    updated_at = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%SZ")

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time'
        ]

    def get_details(self, obj):
        """ Gibt die Offer-Details als Liste von Objekten mit ID und URL zurück """
        request = self.context.get('request')
        return [
            {
                "id": detail.id,
                "url": request.build_absolute_uri(reverse("offer-detail-view", kwargs={"pk": detail.id}))
            }
            for detail in obj.details.all()
        ]

    def get_min_price(self, obj):
        return obj.details.aggregate(min_price=Min('price'))['min_price']

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(min_delivery=Min('delivery_time_in_days'))['min_delivery']

    def update(self, instance, validated_data):
        """ Ermöglicht das Aktualisieren von verschachtelten `details` """
        details_data = validated_data.pop(
            'details', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            instance.details.all().delete()
            for detail_data in details_data:
                OfferDetail.objects.create(
                    offer=instance, **detail_data)

        return instance

    def create(self, validated_data):
        """
        Erstellt ein neues Offer inkl. der verschachtelten OfferDetails.
        """
        details_data = validated_data.pop('details', [])

        offer = Offer.objects.create(**validated_data)

        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)

        return offer
