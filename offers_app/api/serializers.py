from rest_framework import serializers
from offers_app.models import Offer, OfferDetails


class OfferDetailURLSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OfferDetails
        fields = ['id', 'url']


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetails
        # fields = ['revisions']
        # sonst gibts ärger beim erstellen, weil es erforderlich ist
        exclude = ['offer']


class OffersListSerializer(serializers.ModelSerializer):

    details = OfferDetailURLSerializer(many=True)
    # -> das muss ein hyperlinked teil sein!

    class Meta:
        model = Offer
        # sonst gibts ärger beim erstellen, weil es erforderlich ist
        fields = ['id', 'user', 'title', 'details', 'image',
                  'description', 'created_at', 'updated_at']


class OfferWriteSerializer(serializers.ModelSerializer):

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        # sonst gibts ärger beim erstellen, weil es erforderlich ist
        # exclude = ["user"]
        # hier nur die felder, die ich zurückbekommen will:
        fields = ["id", "title", "image", "description", "details"]

    # create brauche ich wegen der nested sache
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetails.objects.create(offer=offer, **detail_data)
        return offer


class SingleOfferListSerializer(serializers.ModelSerializer):

    details = OfferDetailURLSerializer(many=True)

    class Meta:
        model = Offer
        # hier nur die felder, die ich zurückbekommen will:
        fields = ["id", "user", "title", "image", "description",
                  "details", "created_at", "updated_at"]


# serializer zum lesen/GET eines Offers
class OfferReadSerializer(serializers.ModelSerializer):

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        # sonst gibts ärger beim erstellen, weil es erforderlich ist
        exclude = ['created_at', 'updated_at', 'user']

    # create brauche ich wegen der nested sache
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetails.objects.create(offer=offer, **detail_data)
        return offer
