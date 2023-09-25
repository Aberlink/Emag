from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserRegistrationSerializer, BlacklistTokenSerializer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        """Some stuff"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlacklistTokenSerializer

    def post(self, request):
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"detail": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({}, status=status.HTTP_200_OK)
            except AuthenticationFailed as e:
                return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response({"detail": "Token not found."}, status=status.HTTP_404_NOT_FOUND)
