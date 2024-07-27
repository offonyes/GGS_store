from django.db import models
from django.db.models import Count, Q, Sum, F, Case, When


class CategoryManager(models.Manager):
    def get_queryset(self):
        return (super().get_queryset().
                annotate(shoe_count=Count('shoes')))


class ShoeManager(models.Manager):
    def get_queryset(self):
        return (super().get_queryset()
                .annotate(sales_count=Sum('orderitems__quantity'),
                          total_profit=Sum(F('orderitems__quantity')*F('orderitems__price')))
                )
