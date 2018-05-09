#!/usr/bin/env python3.6
import collection
import item
import random


class Container(item.Item):
    """
    A Container item that can hold other items. In addition to the standard item properties,
    it also has a weight allowance that it can hold.
    """
    def __init__(self, name: str, capacity: float, weight: float = 0.0, value: float = 0.0, unique_id: str = None):
        """
        Creates a new Container.

        :param name: Name of the item.
        :param capacity: Maximum weight that can be held.
        :param weight: Weight of the item.
        :param value: Value in GP of the item.
        :param unique_id: Unique identifier for the Container. Defaults to a random number.
        """
        item.Item.__init__(self, name=name, weight=weight, value=value, category='container')
        self.capacity = float(capacity)
        self.contents_weight = 0.0
        self.contents_value = 0.0
        self.contents = {}
        self.id = self._gen_id(unique_id or str(random.getrandbits(40)), self.category, self.name)

    @property
    def full(self) -> bool:
        """Returns if the container is full."""
        return self.contents_weight >= self.capacity

    @property
    def free(self) -> float:
        """Returns the free space in the container"""
        return self.capacity - self.contents_weight

    @property
    def total_weight(self) -> float:
        """Returns total weight of container and its contents."""
        return self.contents_weight + self.weight

    @property
    def total_value(self) -> float:
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
    def _check_search(itm: item.Item, **kwargs) -> bool:
        """
        Checks if an item matches the search conditions.

        :param kwargs: Properties to check.
        :return: True/False
        """
        for key, val in kwargs.items():
            if not hasattr(itm, key):
                return False
            if getattr(itm, key) != val:
                return False
        return True

    def add(self, *collections) -> tuple:
        """
        Adds collections to the container.

        :param collections: Collections or Container to add.
        :return: Tuple of collections that couldn't be added.
        """
        for i, coll in enumerate(collections):
            assert isinstance(coll, collection.Collection) or isinstance(coll, Container), \
                TypeError("collection at {i} is not a Collection or Container".format(i=i))

            if self.contents_weight + coll.weight > self.capacity:
                return collections[i:]

            if isinstance(coll, collection.Collection):
                if coll.id in self.contents:
                    self.contents[coll.id] += coll.quantity
                else:
                    self.contents[coll.id] = coll.__copy__()
                    self.contents[coll.id].parent = self
            else:
                self.contents[coll.id] = coll
                self.contents[coll.id].parent = self
            self.update()

        return ()

    def sub(self, collection_id: str) -> bool:
        """
        Removes a collection in the container.

        :param collection_id: Collection ID to remove.
        :return: True/False if the collection was subtracted.
        """
        if collection_id in self.contents:
            del self.contents[collection_id]
            self.update()
            return True
        return False

    def search(self, **kwargs) -> iter:
        """
        Searches for a set of criteria and yields all matching collections.

        :param kwargs: Properties to search for.
        :return: Yields collections.
        """
        for key in self.contents:
            if self._check_search(self.contents[key], **kwargs):
                yield self.contents[key]
            if isinstance(self.contents[key], Container):
                for i in self.contents[key].search(**kwargs):
                    yield i

    def __str__(self, offset='\t') -> str:
        s = f'{self.name} ({self.contents_weight:.2f}/{self.capacity:.2f}):'

        for i in self.contents:
            s += '\n'+offset+'|'
            if isinstance(self.contents[i], Container):
                s += '-- ' + self.contents[i].__str__(offset=offset+'|\t')
            else:
                s += '-- ' + str(self.contents[i])

        return s


class MagicContainer(Container, item.MagicItem):
    """
    A Magic Container item that can hold other items. In addition to the standard item properties,
    it also has a weight allowance that it can hold. The weight of a MagicContainer remains fixed.
    """
    def __init__(self, name: str, magic: str, capacity: float, weight: float = 0.0, value: float = 0.0,
                 unique_id: str = None, dmg: int = None):
        """
        Creates a new Container.

        :param name: Name of the item.
        :param capacity: Maximum weight that can be held.
        :param weight: Weight of the item.
        :param value: Value in GP of the item.
        :param unique_id: Unique identifier for the Container. Defaults to a random number.
        """
        Container.__init__(self, name=name, capacity=capacity)
        item.MagicItem.__init__(self, name=name, magic=magic, weight=weight, value=value, category='container', dmg=dmg)

        self.id = self._gen_id(unique_id or str(random.getrandbits(40)), self.category, self.name, self.magic)

    @property
    def total_weight(self) -> float:
        """Returns total weight of container and its contents."""
        return self.weight

    def __str__(self, offset='\t') -> str:
        s = f'{self.name} {self.magic} ({self.contents_weight}/{self.capacity}):'

        for i in self.contents:
            s += '\n'+offset+'|'
            if isinstance(self.contents[i], Container):
                s += '-- ' + self.contents[i].__str__(offset=offset+'|\t')
            else:
                s += '-- ' + str(self.contents[i])

        return s


class Player(Container):
    """
    A Container that represents a player (or NPCs) inventory.
    """
    def __init__(self, name: str, capacity: float):
        """
        Creates a new Player.

        :param name: Name of the character.
        :param capacity: Carrying capacity.
        """
        super(Player, self).__init__(name='player', capacity=capacity, weight=0.0, value=0.0, unique_id=name)
        self.player_name = name

    @property
    def inventory(self) -> dict:
        return self.contents

    def __str__(self, offset='\t') -> str:
        s = f'{self.player_name} ({self.contents_weight}/{self.capacity}):'

        for i in self.contents:
            s += '\n'+offset+'|'
            if isinstance(self.contents[i], Container):
                s += '-- ' + self.contents[i].__str__(offset=offset+'|\t')
            else:
                s += '-- ' + str(self.contents[i])

        return s


class Store(Container):
    """
    A Container that represents storage (house, bank,...) with unlimited capacity.
    """
    def __init__(self, name: str):
        """
        Creates a new Store.

        :param name: Name of the store.
        """
        super(Store, self).__init__(name=name, capacity=0.0, weight=0.0, value=0.0)

    @property
    def full(self) -> bool:
        """Returns if the container is full."""
        return False

    @property
    def free(self) -> float:
        """Returns the free space in the container"""
        return self.capacity - self.contents_weight

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
        self.capacity = contents_weight

    def add(self, *collections) -> tuple:
        """
        Adds collections to the container.

        :param collections: Collections or Container to add.
        :return: Tuple of collections that couldn't be added.
        """
        for i, coll in enumerate(collections):
            assert isinstance(coll, collection.Collection) or isinstance(coll, Container), \
                TypeError("collection at {i} is not a Collection or Container".format(i=i))

            if isinstance(coll, collection.Collection):
                if coll.id in self.contents:
                    self.contents[coll.id] += coll.quantity
                else:
                    self.contents[coll.id] = coll.__copy__()
                    self.contents[coll.id].parent = self
            else:
                self.contents[coll.id] = coll
                self.contents[coll.id].parent = self
            self.update()

        return ()
