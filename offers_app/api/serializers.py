from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from django.db.models import Min
from django.urls import reverse


class OfferDetailURLSerializer(serializers.ModelSerializer):
    """ Serializer für ein OfferDetail mit ID & URL """
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        """ Erstellt die absolute URL für ein OfferDetail """
        request = self.context.get('request')
        return request.build_absolute_uri(reverse("offer-detail-view", kwargs={"pk": obj.id}))


class OfferDetailFullSerializer(serializers.ModelSerializer):
    """ Vollständiger Serializer für OfferDetail (nur für POST) """
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type']


class OfferDetailSerializer(serializers.ModelSerializer):
    """ Serializer für eine vollständige OfferDetail-Darstellung für die Einzel-Detail-View """
    class Meta:
        model = OfferDetail
        fields = '__all__'  # Falls wir alle Felder brauchen


class OfferSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(source='creator', read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time'
        ]

    def get_details(self, obj):
        """ Entscheidet, ob die OfferDetails als URLs oder als vollständige Objekte zurückgegeben werden """
        request = self.context.get('request')

        # 🛠 **Wenn POST, dann komplette Detail-Infos zurückgeben**
        if request and request.method == "POST":
            return OfferDetailFullSerializer(obj.details.all(), many=True).data

        # 🛠 **Wenn GET (List/Detail-View), dann nur URLs zurückgeben**
        return OfferDetailURLSerializer(obj.details.all(), many=True, context={'request': request}).data

    def get_min_price(self, obj):
        return obj.details.aggregate(min_price=Min('price'))['min_price']

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(min_delivery=Min('delivery_time_in_days'))['min_delivery']

    def create(self, validated_data):
        """ Erstellt ein Angebot mit OfferDetails und gibt die vollständigen OfferDetails in der Response zurück """
        details_data = validated_data.pop('details', [])  # Details extrahieren
        offer = Offer.objects.create(**validated_data)

        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)

        # 🔥 Wichtig: `context={'request': self.context.get("request")}` weitergeben, damit die Details richtig formatiert sind
        return offer
