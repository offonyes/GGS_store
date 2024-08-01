from django.db import transaction
from rest_framework import viewsets, permissions, filters, status, pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from order_app.models import Order, OrderItem, Cart, CartItem
from order_app.serializers import OrderSerializer, CartSerializer, CartItemSerializer
from shoe_app.models import Shoe


class BasicPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 25


@extend_schema(tags=['Order'], description='Retrieve user orders and create a order.')
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.OrderingFilter,)
    http_method_names = ['get', 'post']
    ordering = ['-date_ordered']

    def get_queryset(self):
        qs = self.queryset.filter(user=self.request.user)
        return qs.prefetch_related('orderitems')

    def create(self, request, *args, **kwargs):
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


@extend_schema(tags=['Cart'], description='Retrieve user cart.')
class CartViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.OrderingFilter,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).prefetch_related('cartitems')

    @extend_schema(tags=['Cart'], description='Add items to cart.')
    @action(detail=False, methods=['post'], url_path='add-item', serializer_class=CartItemSerializer)
    def add_item(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        data = request.data.copy()

        data['cart'] = cart.id

        shoe_id = data.get('shoe')
        shoe = get_object_or_404(Shoe, id=shoe_id)
        data['price'] = shoe.discount_price if (shoe.discount_price < shoe.base_price and
                                                shoe.discount_price != 0) else shoe.base_price

        serializer = CartItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(tags=['Cart'], description='Remove items from cart.')
    @action(detail=True, methods=['delete'])
    def remove_item(self, request, pk=None):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        cart_item = get_object_or_404(CartItem, cart=cart, id=pk)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
