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
        super(Container, self).__init__(name, weight, value, category='container')
        self.capacity = capacity
        self.contents_weight = 0
        self.contents_value = 0
        self.contents = {}
        self.id = self._gen_id(unique_id or str(random.getrandbits(40)), self.category, self.name)

    @property
    def full(self):
        """Returns if the container is full."""
        return self.contents_weight >= self.capacity

    @property
    def free(self):
        """Returns the free space in the container"""
        return self.capacity - self.contents_weight

    @property
    def total_weight(self):
        """Returns total weight of container and its contents."""
        return self.contents_weight + self.weight

    @property
    def total_value(self):
        """Returns total value of container and its contents."""
        return self.contents_value + self.value

    def update(self):
        """
        Updates the current_weight, value, and weight properties
        as items are added to the container.
        """
        contents_weight = 0
        contents_value = 0

        for key in self.contents:
            if isinstance(self.contents[key], Container):
                self.contents[key].update()
                contents_weight += self.contents[key].total_weight
                contents_value += self.contents[key].total_value
            else:
                contents_weight += self.contents[key].weight
                contents_value += self.contents[key].value

        self.contents_weight = contents_weight
        self.contents_value = contents_value

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
                TypeError("collection at {i} is not a Collection or Container".format(i=i))

            if self.contents_weight + collection.weight > self.capacity:
                return collections[i:]

            if isinstance(collection, Collection):
                if collection.id in self.contents:
                    self.contents[collection.id] += collection.quantity
                else:
                    self.contents[collection.id] = collection.__copy__()
            else:
                self.contents[collection.id] = collection
            self.update()

        return []

    def sub(self, collection_id):
        """
        Subtracts a collection in the container.

        :param collection_id: Collection ID to remove.
        :return: True/False if the collection was subtracted.
        """
        if collection_id in self.contents:
            del self.contents[collection_id]
            self.update()
            return True
        return False

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

    @property
    def total_weight(self):
        """Returns total weight of container and its contents."""
        return self.weight


class Player(Container):
    """
    A Container that represents a player (or NPCs) inventory.
    """
    def __init__(self, name, capacity):
        """
        Creates a new Player.

        :param name: Name of the character.
        :param capacity: Carrying capacity.
        """
        super(Player, self).__init__(name='character', capacity=capacity, weight=0, value=0, unique_id=name)

    @property
    def inventory(self):
        return self.contents


class Inventory(Container):
    """
    A Container representing an entire inventory.
    """
    def __init__(self):
        super(Inventory, self).__init__(name='inventory', capacity=0)

    def update(self):
        """
        Updates the current_weight, value, and weight properties
        as items are added to the container.
        """
        contents_weight = 0
        contents_value = 0
        capacity = 0

        for key in self.contents:
            self.contents[key].update()
            capacity += self.contents[key].capacity
            contents_weight += self.contents[key].total_weight
            contents_value += self.contents[key].total_value

        self.contents_weight = contents_weight
        self.contents_value = contents_value
        self.capacity = capacity

    def add(self, *containers):
        """
        Adds containers to the inventory.

        :param containers: Containers to add.
        """
        for i, container in enumerate(containers):
            assert isinstance(container, Container), TypeError("collection at {i} is not a Collection".format(i=i))

            self.contents[container.id] = container
            self.update()

    def sub(self, container_id):
        """
        Subtracts a collection in the container.

        :param container_id: Container ID to remove.
        :return: True/False if the container was subtracted.
        """
        if container_id in self.contents:
            del self.contents[container_id]
            self.update()
            return True
        return False
