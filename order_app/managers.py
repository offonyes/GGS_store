from django.db import models
from django.db.models import Count, Q, Sum, F, Case, When


class OrderManager(models.Manager):
    def get_queryset(self):
        return (super().get_queryset().
                annotate(items=Sum('orderitems__quantity'),
                         total_price=Sum(F('orderitems__quantity') * F('orderitems__price')))
                )


class CartManager(models.Manager):
    def get_queryset(self):
        return (super().get_queryset().
                annotate(items=Sum('cartitems__quantity'),
                         total_price=Sum(F('cartitems__quantity') * F('cartitems__price')))
                )
