from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        try:
            if serializer.is_valid():
                saved_account = serializer.save()
                token, created = Token.objects.get_or_create(
                    user=saved_account)

                data = {
                    'token': token.key,
                    'username': saved_account.username,
                    'email': saved_account.email,
                    'user_id': saved_account.id  # user_id zurückgeben
                }

                return Response(data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Fehler bei der Registrierung:", str(e))
            return Response(
                {"error": "Interner Serverfehler. Bitte später erneut versuchen."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            if serializer.is_valid():
                user = serializer.validated_data['user']
                token, created = Token.objects.get_or_create(user=user)

                data = {
                    'token': token.key,
                    'username': user.username,
                    'user_id': user.id,
                    'email': user.email
                }

                return Response(data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Fehler beim Login:", str(e))
            return Response(
                {"error": "Interner Serverfehler. Bitte später erneut versuchen."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
