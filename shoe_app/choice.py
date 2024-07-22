from django.utils.translation import gettext_lazy as _
from django.db import models


class GenderStatus(models.IntegerChoices):
    MALE = 1, _('Male')
    FEMALE = 2, _('Female')
    # Unisex = 3, _('Unisex')



