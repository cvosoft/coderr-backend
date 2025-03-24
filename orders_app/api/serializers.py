from rest_framework import serializers
from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):

    # zusatzfelder, wo was berechet wird
    title = serializers.SerializerMethodField()
    revisions = serializers.SerializerMethodField()
    delivery_time_in_days = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    offer_type = serializers.SerializerMethodField()

    def get_revisions(self, obj):
        return obj.offerdetails.revisions
    
    def get_delivery_time_in_days(self, obj):
        return obj.offerdetails.delivery_time_in_days

    def get_price(self, obj):
        return obj.offerdetails.price        

    def get_features(self, obj):
        return obj.offerdetails.features    

    def get_offer_type(self, obj):
        return obj.offerdetails.offer_type         

    def get_title(self, obj):
        return obj.offerdetails.offer.title  #hier titel des OFFERS!!

    class Meta:
        model = Order
        fields = '__all__'
