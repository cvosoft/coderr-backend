from rest_framework import serializers
from offers_app.models import Offer, OfferDetails
from django.db.models import Min
from profiles_app.models import UserProfile


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

    # zusatzfelder, wo was berechet wird
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        # sonst gibts ärger beim erstellen, weil es erforderlich ist
        fields = ['id', 'user', 'title', 'details', 'image',
                  'description', 'created_at', 'updated_at',
                  'min_price', 'min_delivery_time',
                  'user_details']

    def get_min_price(self, obj):
        return obj.details.aggregate(min_price=Min('price'))['min_price']

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(min_time=Min('delivery_time_in_days'))['min_time']

    def get_user_details(self, obj):
        try:
            #user_id ist der automatisch erzeugte Feldname für einen ForeignKey
            profile = UserProfile.objects.get(
                user_id=obj.user_id)
        except UserProfile.DoesNotExist:
            return {}

        return {
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "username": profile.username,
        }


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
