from django.db import models
from django.contrib.auth.models import User


class System(models.Model):
    """
    Model for game systems. Includes the name and its base_currency.
    """
    name = models.TextField(null=False)
    base_currency = models.TextField(null=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    """
    Model for base item types and the relevent Item fields used for that type.
    """
    name = models.TextField(null=False)
    fields = models.TextField(null=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Model for item categories. Categories are linked to an item type but are specific to
    game systems (e.g. Potion -> Consumable Type).
    """
    name = models.TextField(null=False)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    system = models.ForeignKey(System, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.system.name} | {self.name}'


class Item(models.Model):
    """
    Model for Items in a game system. These are the default items from the ruleset.
    """
    name = models.TextField(null=False)
    value = models.FloatField(null=False)
    weight = models.FloatField(null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    magic = models.BooleanField(null=False)
    capacity = models.FloatField(null=True)
    uses = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.system.name} | {self.name}'


class PortableHole(models.Model):
    """
    Model for PortableHoles. Each row represents a different game. These belong to Users
    """
    name = models.TextField(null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    contents = models.TextField(null=False, default='{}')

    def __str__(self):
        return f'{self.system} | {self.name}'


class UserItem(Item):
    """
    Models that extends Item for user added content. These are tied to PortableHole sessions.
    """
    portablehole = models.ForeignKey(PortableHole, on_delete=models.CASCADE)
