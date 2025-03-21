from rest_framework import serializers
from offers_app.models import Offer, OfferDetails


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetails
        # fields = '__all__'
        exclude = ['offer']  # sonst gibts ärger beim erstellen


class OfferSerializer(serializers.ModelSerializer):

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = '__all__'

    # create brauche ich wegen der nested sache
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetails.objects.create(offer=offer, **detail_data)
        return offer
