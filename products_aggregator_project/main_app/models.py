import uuid
from django.db import models


class Node(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, max_length=40, blank=True)
    name = models.CharField(null=False, blank=False, max_length=100)
    price = models.IntegerField(null=True, blank=True)
    updated_dt = models.DateTimeField(null=True, blank=True, max_length=30)
    type = models.CharField(null=False, blank=False, max_length=100)
