from rest_framework import serializers
from backend_app.models import UserProfile
from django.contrib.auth.models import User



class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(
        choices=UserProfile.USER_TYPES, required=True)  # <-- Type hinzufügen

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, data):
        """
        - Stellt sicher, dass die Passwörter übereinstimmen.
        - Prüft, ob die E-Mail bereits existiert.
        """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match!'})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {'email': 'This email is already in use!'})

        return data

    def create(self, validated_data):
        # Entferne `type` vor dem User-Speichern
        user_type = validated_data.pop('type')
        # Entferne das wiederholte Passwort
        validated_data.pop('repeated_password')

        user = User.objects.create_user(**validated_data)  # User erstellen
        # UserProfile mit `type` erstellen
        UserProfile.objects.create(user=user, type=user_type)

        return user
