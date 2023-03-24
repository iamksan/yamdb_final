from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


class User(AbstractUser):
    CHOICES = (
        (USER, 'пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'админ')
    )
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=15, choices=CHOICES, default=USER)
    confirmation_code = models.CharField(max_length=255, blank=True, null=True)
    USERNAME_FIELD = 'username'

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_follow'
            ),
        )

    def __str__(self):
        return self.username[:15]

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR
