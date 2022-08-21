from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

USER_TYPES = [
    ('g', 'Golden'),
    ('s', 'Silver'),
    ('t', 'Typical')
]


class Profile(models.Model):
    """Profile model for each User"""

    type = models.CharField(max_length=1, choices=USER_TYPES, default='t',
                            help_text='type of user Golden, Silver, Typical')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
