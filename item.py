#!/usr/bin/env python3.6
class Item:
    """
    An Item. Contains properties for the item's name, weight, value, and category.
    """
    def __init__(self, name: str, weight: float = 0.0, value: float = 0.0, category: str = 'misc'):
        """
        Creates a new Item.

        :param name: Name of the item.
        :param weight: Weight of the item.
        :param value: Value in GP of the item.
        :param category: The kind of item to create.
        """
        self.name = name
        self.weight = float(weight)
        self.value = float(value)
        self.category = category
        self.id = self._gen_id(category, name)
        self.m = False
        self.parent = None

    @staticmethod
    def _gen_id(*args: str) -> str:
        """
        Generates an id for the Item by appending the args together.

        :param args: Items to join together.
        :return: String of args joined by a '|'
        """
        return '|'.join(args)

    def __str__(self) -> str:
        return self.name


class MagicItem(Item):
    """
    A Magical Item that extends the base item class. This has additional properties
    for the item's magic properties.
    """
    def __init__(self, name: str, magic: str, weight: float = 0.0, value: float = 0.0,
                 category: str = 'misc', dmg: int = None):
        """
        Creates a new MagicItem.

        :param name: Name of the item.
        :param magic: Description of Magic.
        :param weight: Weight of the item.
        :param value: Value in GP of the item.
        :param category: The kind of item to create.
        :param dmg: (Optional) Page reference of item.
        """
        super(MagicItem, self).__init__(name, weight, value, category)
        self.magic = magic
        self.dmg = dmg
        self.id = self._gen_id(category, name, magic)
        self.m = True

    def __str__(self) -> str:
        return f'{self.name} {self.magic}'

