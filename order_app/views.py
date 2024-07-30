from django.db import transaction
from rest_framework import viewsets, permissions, filters, status, pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from order_app.models import Order, OrderItem, Cart, CartItem
from order_app.serializers import OrderSerializer, OrderItemSerializer, CartSerializer, CartItemSerializer, DetailOrderSerializer
from shoe_app.models import Shoe


class BasicPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 25


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.OrderingFilter,)
    http_method_names = ['get', 'post']
    ordering = ['-date_ordered']

    def get_queryset(self):
        qs = self.queryset.filter(user=self.request.user)
        return qs

    def create(self, request, *args, **kwargs):
        print(self.request.user)
        print(request.user)
        user = request.user
        cart = Cart.objects.filter(user=user).first()

        if not cart or not cart.cartitems.exists():
            return Response({'detail': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order = Order.objects.create(user=user)
            cart_items = cart.cartitems.all()

            order_items = [
                OrderItem(
                    order=order,
                    shoe=cart_item.shoe,
                    size=cart_item.size,
                    color=cart_item.color,
                    quantity=cart_item.quantity,
                    price=cart_item.price
                )
                for cart_item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)
            cart.cartitems.all().delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = BasicPagination

    def list(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cartitems.all().order_by('id')

        paginator = self.pagination_class()
        paginated_cart_items = paginator.paginate_queryset(cart_items, request)

        serializer = CartItemSerializer(paginated_cart_items, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        shoe_id = request.data.get('shoe')
        size = request.data.get('size')
        color = request.data.get('color')
        price = request.data.get('price')
        quantity = request.data.get('quantity', 1)

        if not shoe_id or not size or not color or not price:
            return Response({'detail': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        shoe = get_object_or_404(Shoe, id=shoe_id)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            shoe=shoe,
            size=size,
            color=color,
            price=price,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def remove_item(self, request, pk=None):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        cart_item = get_object_or_404(CartItem, cart=cart, id=pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
