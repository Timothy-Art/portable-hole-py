#!/usr/bin/env python3
class Item:
    """
    An Item. Contains properties for the item's name, weight, value, and kind.
    """

    def __init__(self, name, weight, value, kind):
        """
        Creates a new Item.

        :param name: Name of the item.
        :param weight: Weight of the item.
        :param value: Value in GP of the item.
        :param kind: The kind of item to create.
        """

        self.name = name
        self.weight = float(weight)
        self.value = float(value)
        self.kind = kind

    def __str__(self):
        return self.name


class MagicItem(Item):
    """
    A Magical Item that extends the base item class. This has additional properties
    for the item's magic properties.
    """

    def __init__(self, magic, dmg=None, **kwargs):
        """
        Creates a new MagicItem.

        :param magic: Description of Magic.
        :param dmg: (Optional) Page reference of item.
        :param kwargs: Parameters to pass to Item constructor.
        """

        self.magic = magic
        self.dmg = dmg
        super().__init__(**kwargs)

    def __str__(self):
        return self.name + ' ' + self.magic


class Consumable(MagicItem):
    """
    A Consumable item, like a potion or oil, that has a number of uses associated with it.
    """

    def __init__(self, uses, **kwargs):
        """
        Creates a new Consumable.

        :param uses: Number of uses.
        :param kwargs: Parameters to pass to MagicItem and Item constructors.
        """

        self.uses = int(uses)
        self.usage = 0
        self.empty = 0 <= uses
        super().__init(**kwargs)

    def remaining(self):
        """
        Returns the remaining Consumable.

        :return: How many uses are left.
        """

        return self.uses - self.usage

    def use(self, n=1):
        """
        Uses up a consumable.

        :param n: How many uses, defaults to 1
        :return: True/False if the item was used.
        """

        if self.usage+n <= self.uses:
            self.usage += n
            self.empty = self.usage <= self.uses

            return True

        return False

    def use_all(self):
        """
        Uses up the remaining Consumable.

        :return: How many uses were left
        """

        if not self.empty:
            usage = self.usage
            self.usage = self.uses
            self.empty = True

            return self.usage - usage

        return 0