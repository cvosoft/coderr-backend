from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio']


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

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError(
                {'error': 'passwords dont match!'})

        # email darf nur einmal vorkommen
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError(
                {'error': 'Email gibt es schon!'})

        account = User(
            email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(pw)
        account.save()
        return account

    def create(self, validated_data):
        # Entferne `type` vor dem User-Speichern
        user_type = validated_data.pop('type')
        # Entferne das wiederholte Passwort
        validated_data.pop('repeated_password')

        user = User.objects.create_user(**validated_data)  # User erstellen
        # UserProfile mit `type` erstellen
        UserProfile.objects.create(user=user, type=user_type)

        return user
