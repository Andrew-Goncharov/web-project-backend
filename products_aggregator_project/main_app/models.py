from django.db import models


class Node(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, max_length=30, blank=True)
    name = models.CharField(null=False, blank=False, max_length=100)
    price = models.IntegerField(null=True, blank=True)
    updated_dt = models.DateField(null=False, blank=False, max_length=30)
    type = models.CharField(null=False, blank=False, max_length=100)
