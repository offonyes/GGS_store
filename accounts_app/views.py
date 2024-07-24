from rest_framework.response import Response
from rest_framework import generics, status, permissions

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts_app.models import CustomUser
from accounts_app.serializers import RegisterSerializer, CustomUserSerializer


@extend_schema(tags=['User'], description='User Registration Api', methods=['post'])
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(tags=['User'], description='User profile info Api', methods=['get'])
class ProfileView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def get_queryset(self):
        qs = self.queryset
        qs = qs.filter(email=self.request.user)
        return qs
