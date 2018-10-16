from django.db import models


class Inventory(models.Model):
    inv_id = models.BigIntegerField()
    portable_hole = models.TextField()


class Campaign(models.Model):
    name = models.TextField()
    module = models.SmallIntegerField()
    inv_id = models.ForeignKey(Inventory, on_delete=models.CASCADE)
