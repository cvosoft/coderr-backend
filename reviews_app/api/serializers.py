from rest_framework import serializers
from reviews_app.models import Reviews


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"

        # fields = ["id",]


class ReviewsPOSTSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        # nur drei felder rausschicken
        fields = ["business_user", "rating", "description"]
