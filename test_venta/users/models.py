from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):
    __status = (
        (2, "aprobado"),
        (3, "deshabilitado"),
        (1, "pending"),
    )

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    last_name = models.CharField(_('Name of User'), blank=True, max_length=255)
    address = models.TextField(null=True)
    status = models.SmallIntegerField(
        default=1, choices=__status)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
