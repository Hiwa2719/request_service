from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
import uuid
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
    bill_id = models.UUIDField(default=uuid.uuid4, editable=False, blank=True)
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    state = models.CharField(max_length=2, choices=STATES, default='CR', blank=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    user_extra_description = models.TextField(blank=True)
    staff_extra_description = models.TextField(blank=True)
    wage = models.ForeignKey(Wage, on_delete=models.DO_NOTHING, blank=True)
    photo = models.ImageField(validators=[max_size_validator], blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [('only_check_bills', 'can see only bills with check status')]

    def __str__(self):
        return f'{self.user.username}-{self.service.name}'


@receiver(pre_save, sender=Bill)
def state_email_sender(sender, instance, **kwargs):
    try:
        bill = sender.objects.get(id=instance.id)
    except Bill.DoesNotExist:
        return
    if bill.state != instance.state and instance.state == 'DF':
        message = render_to_string('accounts/deficit_issue.html', {
            'bill': instance
        })
        send_mail(subject='Bill deficit', message='there is issue with your bill',
                  from_email='hiahmadyan@gmail.com', recipient_list=[instance.user.email], html_message=message)
