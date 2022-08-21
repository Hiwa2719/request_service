from django.db import models
from accounts.models import USER_TYPES


class Service(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Wage(models.Model):
    user_type = models.CharField(max_length=1, choices=USER_TYPES, default='t')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    percentage = models.IntegerField()

    class Meta:
        constraints = [models.constraints.UniqueConstraint(fields=['user_type', 'service'], name='unique_wage')]

    def __str__(self):
        return f'{self.service.name}-{self.get_user_type_display()}'
