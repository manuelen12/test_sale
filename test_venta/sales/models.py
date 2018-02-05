from django.db import models
from django.conf import settings
import uuid


class Sales(models.Model):

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    amount = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='sales_user', null=True)
    status = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'sales'
        db_table = 'sales'

    def __str__(self):
        return self.uuid
