#!/usr/bin/env python3
import random

from item import Item, MagicItem
from collection import Collection


class Container(Item):
    """
    A Container item that can hold other items. In addition to the standard item properties,
    it also has a weight allowance that it can hold.
    """
    def __init__(self, name, capacity, weight=0, value=0, unique_id=None):
        """
        Creates a new Container.

        :param name: Name of the item.
        :param capacity: Maximum weight that can be held.
        :param weight: Weight of the item.
        :param value: Value in GP of the item.
        :param unique_id: Unique identifier for the Container. Defaults to a random number.
        """
        super().__init__(name, weight, value, category='container')
        self.capacity = capacity
        self.current_weight = 0
        self.contents = {}
        self.id = self._gen_id(unique_id or str(random.getrandbits(40)), self.category, self.name)

    @property
    def full(self):
        """Returns if the container is full."""
        return self.current_weight >= self.capacity

    @property
    def free(self):
        """Returns the free space in the container"""
        return self.capacity - self.current_weight

    def _update(self, collection):
        """
        Updates the current_weight, value, and weight properties
        as items are added to the container.

        :param collection: Collection being added.
        """
        self.current_weight += collection.weight
        self.value += collection.value
        self.weight += collection.weight

    def _sub_update(self, collection_id, n):
        """
        Updates the current_weight, value, and weight properties
        for items that are removed from the container.

        :param collection_id: Collection ID to subtract from.
        :param n: Amount to subtract.
        """
        self.current_weight -= self.contents[collection_id].item.weight * n
        self.value -= self.contents[collection_id].item.value * n
        self.weight -= self.contents[collection_id].item.weight * n

    @staticmethod
    def _check_search(item, magic, item_id, category):
        """
        Checks if an item matches the search conditions.

        :param item: Collection to check.
        :param magic: True/False if magic.
        :param item_id: Item ID to match.
        :param category: List of categories to check for.
        :return: True/False
        """
        if magic:
            if not isinstance(item.item, MagicItem):
                return False
        if item_id is not None:
            if item.id != item_id:
                return False
        if category is not None:
            if item.item.category not in category:
                return False

        return True

    def add(self, *collections):
        """
        Adds collections to the container.

        :param collections: Collections to add.
        :return: List of collections that couldn't be added.
        """
        for i, collection in enumerate(collections):
            assert isinstance(collection, Collection) or isinstance(collection, Container), \
                TypeError("collection at {i} is not a Collection".format(i=i))

            if self.current_weight + collection.weight > self.capacity:
                print('over limit')
                return collections[i:]

            if isinstance(collection, Collection):
                if collection.id in self.contents:
                    self.contents[collection.id] += collection.quantity
                else:
                    self.contents[collection.id] = collection.__copy__()
            else:
                self.contents[collection.id] = collection
            self._update(collection)

        return []

    def sub(self, collection_id, n=None):
        """
        Subtracts items from a collection in the container.

        :param collection_id: Collection ID to subtract from.
        :param n: Amount to subtract.
        :return: The quantity subtracted.
        """
        qty = 0
        if collection_id in self.contents:
            try:
                if n is None:
                    qty = self.contents[collection_id].quantity
                    self.contents[collection_id] -= qty
                else:
                    qty = n
                    self.contents[collection_id] -= n
            except ValueError:
                qty = self.contents[collection_id].quantity
                self.contents[collection_id] -= qty
        self._sub_update(collection_id, qty)

        return qty

    def search(self, magic=False, item_id=None, category=None):
        """
        Searches for a set of criteria and yields all matching collections.

        :param magic: True/False if magic item.
        :param item_id: String with item id to find.
        :param category: List of categories to search for.
        :return: Yields collections.
        """
        for key in self.contents:
            if isinstance(self.contents[key], Container):
                for i in self.contents[key].search(magic, item_id, category):
                    yield i
            else:
                if self._check_search(self.contents[key], magic, item_id, category):
                    yield self.contents[key]

    def __str__(self, offset='\t'):
        s = self.name + ':'

        for i in self.contents:
            s += '\n'+offset+'|'
            if isinstance(self.contents[i], Container):
                s += '-- ' + self.contents[i].__str__(offset=offset+'|\t')
            else:
                s += '-- ' + str(self.contents[i])

        return s


class MagicContainer(Container, MagicItem):
    """
    A Magic Container item that can hold other items. In addition to the standard item properties,
    it also has a weight allowance that it can hold. The weight of a MagicContainer remains fixed.
    """
    def __init__(self, name, magic, capacity, weight=0, value=0, unique_id=None, dmg=None):
        """
        Creates a new Container.

        :param name: Name of the item.
        :param capacity: Maximum weight that can be held.
        :param weight: Weight of the item.
        :param value: Value in GP of the item.
        :param unique_id: Unique identifier for the Container. Defaults to a random number.
        """
        Container.__init__(self, name, capacity)
        MagicItem.__init__(self, name, magic, weight, value, category='container', dmg=dmg)

        self.id = self._gen_id(unique_id or str(random.getrandbits(40)), self.category, self.name)

    def _update(self, collection):
        """
        Updates the current_weight and value properties
        as items are added to the container.

        :param collection: Collection being added.
        """
        self.current_weight += collection.weight
        self.value += collection.value

    def _sub_update(self, collection_id, n):
        """
        Updates the current_weight, value, and weight properties
        for items that are removed from the container.

        :param collection_id: Collection ID to subtract from.
        :param n: Amount to subtract.
        """
        self.current_weight -= self.contents[collection_id].item.weight * n
        self.value -= self.contents[collection_id].item.value * n
