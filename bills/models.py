from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from services.models import Service, Wage

User = get_user_model()


def max_size_validator(value):
    """
    this validator checks for file size
    """

    limit = 1 * 1024 * 1024  # 1MB
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1 MB.')


class Bill(models.Model):
    STATES = [
        ('CR', 'Created'),
        ('DF', 'Deficit'),
        ('CK', 'Check'),
        ('FN', 'Finalized'),
    ]

    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    state = models.CharField(max_length=2, choices=STATES)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    user_extra_description = models.TextField()
    staff_extra_description = models.TextField()
    wage = models.ForeignKey(Wage, on_delete=models.DO_NOTHING)
    photo = models.ImageField(validators=[max_size_validator])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}-{self.service.name}'
