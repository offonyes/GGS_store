from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from shoe_app.choice import GenderStatus


class Category(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=100, null=False, blank=False,
                            unique=True)
    gender = models.IntegerField(choices=GenderStatus, default=GenderStatus.MALE, verbose_name=_('Gender'))

    def __str__(self):
        return self.name


def shoe_directory_path(instance, filename):
    return "shoe/images/shoe_{id}/{file}".format(id=instance.id, file=filename)


class Shoe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='shoes', verbose_name=_('Category'))
    name = models.CharField(max_length=100, verbose_name=_('Name'), null=False, blank=False)  # Add Unique or not
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'), default=0, null=False,
                                     blank=False)
    # MB add some discount for this
    image = models.ImageField(upload_to=shoe_directory_path, null=True, blank=True, verbose_name=_('Image'))

    class Meta:
        verbose_name = _('Shoe')
        verbose_name_plural = _('Shoes')

    def __str__(self):
        return self.name


class ShoeSize(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, related_name='sizes', verbose_name=_('Shoe'))
    size = models.IntegerField(default=40, verbose_name=_('Size'), null=False, blank=False)
    available_amount = models.IntegerField(default=0, verbose_name=_('Available amount'), null=False, blank=False)

    class Meta:
        verbose_name = _('Shoe Size')
        verbose_name_plural = _('Shoes Sizes')

    def __str__(self):
        return self.size


class Review(models.Model):
    user = models.ForeignKey('accounts_app.CustomUser', on_delete=models.CASCADE, related_name='reviews',
                             verbose_name=_('User'))
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('Shoe'))
    rating = models.PositiveSmallIntegerField(default=5, verbose_name=_('Rating'), null=False, blank=False,
                                              validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.TextField(null=True, blank=True, verbose_name=_('Comment'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Created at'))

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ('-created_at',)

    def __str__(self):
        return f"Review by {self.user.username} for {self.shoe.name}"