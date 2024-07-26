from django.db import models
from django.utils.translation import gettext_lazy as _

from order_app.choice import StatusChoices


class Order(models.Model):
    user = models.ForeignKey('accounts_app.CustomUser', on_delete=models.CASCADE, related_name='order',
                             verbose_name=_('User'))
    status = models.IntegerField(choices=StatusChoices, default=StatusChoices.PENDING, verbose_name=_('Status'))
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Date Ordered'))

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitem', verbose_name=_('Order'))
    shoe = models.ForeignKey('shoe_app.Shoe', on_delete=models.CASCADE, related_name='orderitem',
                             verbose_name=_('Shoe'))
    size = models.PositiveIntegerField(default=40, verbose_name=_('Size'), null=False, blank=False)
    color = models.CharField(max_length=50, verbose_name=_('Color'), null=False, blank=False)
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'), null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Date Added'))

    def __str__(self):
        return f"{self.quantity} x {self.shoe.name} (Size {self.size})"


class Cart(models.Model):
    user = models.OneToOneField('accounts_app.CustomUser', on_delete=models.CASCADE, related_name='cart',
                                verbose_name=_('User'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Created at'))

    def __str__(self):
        return f"Cart of {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems', verbose_name=_('Cart'))
    shoe = models.ForeignKey('shoe_app.Shoe', on_delete=models.CASCADE, related_name='cartitems',
                             verbose_name=_('Shoe'))
    size = models.PositiveIntegerField(default=40, verbose_name=_('Size'), null=False, blank=False)
    color = models.CharField(max_length=50, verbose_name=_('Color'), null=False, blank=False)
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'), null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Date Added'))

    def __str__(self):
        return f"{self.quantity} x {self.shoe.name} (Size {self.size}) in cart"
