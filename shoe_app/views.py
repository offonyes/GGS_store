from rest_framework import viewsets, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from shoe_app.models import Shoe, Category, Review
from shoe_app.serializers import (ShoeSerializer, CreateShoeSerializer, CategorySerializer, ReviewSerializer,
                                  CreateReviewSerializer)


@extend_schema(tags=['Shoe'], description='Retrieve all shoe categories.',
               parameters=[
                   OpenApiParameter(
                       name='search',
                       type=OpenApiTypes.STR,
                       location=OpenApiParameter.QUERY,
                       description='Filter by category name or gender.',),
                   OpenApiParameter(
                       name='ordering',
                       type=OpenApiTypes.STR,
                       location=OpenApiParameter.QUERY,
                       description='Order by category name or gender.',)
               ])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering = ['id']
    search_fields = ['name', 'gender']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


@extend_schema(tags=['Shoe'], description='Retrieve all shoes.')
class ShoeViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering = ['id']

    def get_queryset(self):
        qs = Shoe.objects.all()
        return qs.select_related('category')

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'review']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return ShoeSerializer
        return CreateShoeSerializer

    @action(detail=True, methods=['get'], url_path='review')
    def review(self, request, pk=None):
        shoe = self.get_object()
        review = Review.objects.filter(shoe=shoe.id).select_related('shoe', 'user').order_by('-created_at')
        page = self.paginate_queryset(review)

        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ReviewSerializer(review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Review'],)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.OrderingFilter,)
    http_method_names = ['get', 'post']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = self.queryset
        qs = qs.filter(user=self.request.user).select_related('shoe', 'user')
        return qs

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return ReviewSerializer
        return CreateReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
