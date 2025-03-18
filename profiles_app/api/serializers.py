from rest_framework import serializers
from profiles_app.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

    def update(self, instance, validated_data):
        user = instance.user

        if "email" in validated_data:
            new_email = validated_data.pop("email")
            user.email = new_email
            user.save()

        return super().update(instance, validated_data)
