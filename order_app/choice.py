from django.utils.translation import gettext_lazy as _
from django.db import models


class StatusChoices(models.IntegerChoices):
    PENDING = 1, _('Pending')
    PROCESSING = 2, _('Processing')
    COMPLETED = 3, _('Completed')
    CANCELLED = 4, _('Cancelled')
