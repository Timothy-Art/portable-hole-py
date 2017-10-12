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
        super().__init__(**kwargs)

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


def get_collection(kind=None):
    """
    Factory function to return a collection class based on the kind requested.

    :param kind: Consumable or None
    :return: Collection class
    """

    if kind == "Consumable":
        base = Consumable
    else:
        base = object

    class Collection(base):
        """
        A Collection of Items, MagicItems, or Consumables of the same type.
        """

        def __init__(self, what, qty):
            """
            Creates a new Collection.

            :param what: The Item, MagicItem, or Consumable to collect.
            :param qty: The number of Items in the collection.
            """
            self.what = what
            self.name = what.name
            self.qty = int(qty)
            self.weight = what.weight * self.qty
            self.value = what.value * self.qty

            self.magical = type(what) == 'MagicItem'
            self.consumable = type(what) == 'Consumable'

            if self.magic:
                self.magic = what.magic

            if self.consumable:
                self.uses = what.uses * self.qty
                self.usage = 0
                self.empty = 0 <= self.uses

        def add(self, qty, item):
            """
            Adds to the collection.

            :param qty: The number of items to add.
            :param item: A supplied item to add, should be used for Consumables only.
            :return: New qty.
            """
            if qty:
                self.qty += qty
                self.weight += qty * self.what.weight
                self.value += qty * self.what.value

                if self.consumable:
                    self.uses += qty * self.what.uses

            elif item:
                assert isinstance(item, type(self.what)), 'Item Mismatch'
                assert item.name == self.what.name, 'Item Mismatch'

                if self.magical:
                    assert item.magic == self.what.magic, 'Item Mismatch'

                self.qty += 1
                self.weight += self.what.weight
                self.value += self.what.value

                if self.consumable:
                    self.uses += item.uses - item.usage

            else:
                raise Exception('No qty or item supplied!')

            return self.qty

        def sub(self, qty):
            """
            Subtracts an item from the collection.

            :param qty: The number of items to subtract.
            :return: New qty.
            """

            assert qty <= self.qty, "Not enough in collection"

            self.qty -= qty
            self.weight -= qty * self.what.weight
            self.value -= qty * self.what.value

            return self.qty

        def is_empty(self):
            """
            Returns if the collection is empty.

            :return: Boolean
            """

            return self.qty == 0

    return Collection
