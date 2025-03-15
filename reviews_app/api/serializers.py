from rest_framework import serializers
from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['business_user', 'rating', 'description']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError(
                "Die Bewertung muss zwischen 1 und 5 liegen.")
        return value
