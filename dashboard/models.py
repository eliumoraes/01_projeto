from django.db import models
import uuid
import re

class Cliente(models.Model):
    name = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=11, null=False)
    email = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    div_id = models.UUIDField(default=uuid.uuid4, editable=True)

    def __str__(self):
        return self.name

