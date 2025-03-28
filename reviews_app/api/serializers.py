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

    def validate(self, data):
        request = self.context['request']
        reviewer = request.user
        business_user = data.get('business_user')

        if Reviews.objects.filter(reviewer=reviewer, business_user=business_user).exists():
            raise serializers.ValidationError(
                "Du hast diesen Anbieter bereits bewertet!")
        return data
