from django.db import models
from django.db.models import Count, Avg


class CategoryManager(models.Manager):
    def get_queryset(self):
        return (super().get_queryset().
                annotate(shoe_count=Count('shoes')))


class ShoeManager(models.Manager):
    def get_queryset(self):
        return (super().get_queryset()
                .annotate(review_avg=Avg('reviews__rating')))
