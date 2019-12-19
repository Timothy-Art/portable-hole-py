import random
from enum import Enum, auto


class ItemCategory(Enum):
    COIN = 1
    GEM = 2
    WEAPON = 3
    ARMOUR = 4
    AMMUNITION = 5
    CONSUMABLE = 6
    CONTAINER = 7
    SUPPLY = 8
    MISC = 9


class Item:
    """
    An Item. Contains properties for the item's name, weight, value, and category.
    """
    def __init__(self, name: str, weight: float = 0.0, value: float = 0.0, category=ItemCategory.MISC):
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
        self.id = self._gen_id(str(category), name)
        self.m = False
        self.parent = None

    @property
    def display_name(self):
        return self.name

    @staticmethod
    def _gen_id(*args: str) -> str:
        """
        Generates an id for the Item by appending the args together.

        :param args: Items to join together.
        :return: String of args joined by a '|'
        """
        return '|'.join(args)

    def to_dict(self) -> dict:
        """
        Returns the item as a dictionary mapping.

        :return: Dictionary.
        """
        out = {
            'type': type(self).__name__,
            'name': self.name,
            'weight': self.weight,
            'value': self.value,
            'category': self.category
        }

        return out

    def __str__(self) -> str:
        return self.display_name

    def __eq__(self, other) -> bool:
        if not other.id == self.id:
            return False
        if not other.weight == self.weight:
            return False
        if not other.value == self.value:
            return False
        return True


class MagicItem(Item):
    """
    A Magical Item that extends the base item class. This has additional properties
    for the item's magic properties.
    """
    def __init__(self, name: str, magic: str, weight: float = 0.0, value: float = 0.0,
                 category=ItemCategory.MISC, dmg: int = None):
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
        self.id = self._gen_id(str(category), name, magic)
        self.m = True

    @property
    def display_name(self):
        return f'{self.name} {self.magic}'

    def to_dict(self) -> dict:
        """
        Returns the item as a dictionary mapping.

        :return: Dictionary.
        """
        out = {
            'type': type(self).__name__,
            'name': self.name,
            'magic': self.magic,
            'weight': self.weight,
            'value': self.value,
            'category': self.category,
            'dmg': self.dmg
        }

        return out


class Collection:
    """
    A collection of Items
    """
    def __init__(self, item, quantity: int = 1):
        """
        Creates a new Collection of a given Item.

        :param item: Item to collect.
        :param quantity: Quantity of Items to start with. Defaults to 1.
        """
        self.item = item
        self.item.parent = self
        self.quantity = quantity
        self.weight = self.item.weight * quantity
        self.value = self.item.value * quantity
        self.id = self.item.id
        self.m = self.item.m
        self.category = self.item.category
        self.name = self.item.name
        self.magic = self.item.magic if self.m else None
        self.parent = None

    @property
    def display_name(self):
        return f'{str(self.item)}  x{self.quantity}'

    def to_dict(self) -> dict:
        """
        Returns the collection as a dictionary mapping.

        :return: Dictionary.
        """
        out = {
            'type': type(self).__name__,
            'item': self.item.to_dict(),
            'quantity': self.quantity
        }

        return out

    def add(self, n: int = 1):
        """
        Adds to the Collection.

        :param n: Quantity to add.
        """
        try:
            n = int(n)
        except TypeError:
            raise TypeError("unsupported operand type for add: {other}".format(other=type(n)))

        assert self.quantity + n >= 0, ValueError("quantity cannot be < 0")
        self.quantity += n
        self.weight += n * self.item.weight
        self.value += n * self.item.value

    def __add__(self, other: int):
        try:
            other = int(other)
        except TypeError:
            raise TypeError("unsupported operand type for +: {other}".format(other=type(other)))

        assert self.quantity + other >= 0, ValueError("quantity cannot be < 0")
        return Collection(item=self.item, quantity=self.quantity + other)

    def __iadd__(self, other: int):
        try:
            other = int(other)
        except TypeError:
            raise TypeError("unsupported operand type for +: {other}".format(other=type(other)))

        assert self.quantity + other >= 0, ValueError("quantity cannot be < 0")
        self.quantity += other
        self.weight += other * self.item.weight
        self.value += other * self.item.value
        return self

    def sub(self, n: int = 1):
        """
        Subtracts from the Collection.

        :param n: Quantity to subtract.
        """
        try:
            n = int(n)
        except TypeError:
            raise TypeError("unsupported operand type for sub: {other}".format(other=type(n)))

        assert self.quantity - n >= 0, ValueError("quantity cannot be < 0")
        self.quantity -= n
        self.weight -= n * self.item.weight
        self.value -= n * self.item.value

    def __sub__(self, other: int):
        try:
            other = int(other)
        except TypeError:
            raise TypeError("unsupported operand type for -: {other}".format(other=type(other)))

        assert self.quantity - other >= 0, ValueError("quantity cannot be < 0")

        return Collection(item=self.item, quantity=self.quantity - other)

    def __isub__(self, other: int):
        try:
            other = int(other)
        except TypeError:
            raise TypeError("unsupported operand type for -=: {other}".format(other=type(other)))

        assert self.quantity - other >= 0, ValueError("quantity cannot be < 0")
        self.quantity -= other
        self.weight -= other * self.item.weight
        self.value -= other * self.item.value
        return self

    def mult(self, n: int = 1):
        """
        Multiplies the Collection.

        :param n: Quantity to multiply by.
        """
        try:
            n = int(n)
        except TypeError:
            raise TypeError("unsupported operand type for add: {other}".format(other=type(n)))

        assert self.quantity * n >= 0, ValueError("quantity cannot be < 0")
        self.quantity *= n
        self.weight = self.quantity * self.item.weight
        self.value = self.quantity * self.item.value

    def __mul__(self, other: int):
        try:
            other = int(other)
        except TypeError:
            raise TypeError("unsupported operand type for *: {other}".format(other=type(other)))

        assert self.quantity * other >= 0, ValueError("quantity cannot be < 0")
        return Collection(item=self.item, quantity=self.quantity * other)

    def __imul__(self, other: int):
        try:
            other = int(other)
        except TypeError:
            raise TypeError("unsupported operand type for *: {other}".format(other=type(other)))

        assert self.quantity * other >= 0, ValueError("quantity cannot be < 0")
        self.quantity *= other
        self.weight = self.quantity * self.item.weight
        self.value = self.quantity * self.item.value
        return self

    def __copy__(self):
        return Collection(self.item, quantity=self.quantity)

    def __eq__(self, other):
        if not other.item == self.item:
            return False
        if not other.quantity == self.quantity:
            return False
        return True

    def __str__(self) -> str:
        return self.display_name


class Container(Item):
    """
    A Container item that can hold other items. In addition to the standard item properties,
    it also has a weight allowance that it can hold.
    """
    def __init__(
        self,
        name: str,
        capacity: float,
        weight: float = 0.0,
        value: float = 0.0,
        unique_id: str = None
    ):
        """
        Creates a new Container.

        :param name: Name of the item.
        :param capacity: Maximum weight that can be held.
        :param weight: Weight of the item.
        :param value: Value in GP of the item.
        :param unique_id: Unique identifier for the Container. Defaults to a random number.
        """
        Item.__init__(self, name=name, weight=weight, value=value, category=ItemCategory.CONTAINER)
        self.capacity = float(capacity)
        self.contents_weight = 0.0
        self.contents_value = 0.0
        self.contents = {}
        self.id = self._gen_id(unique_id or str(random.getrandbits(40)), str(self.category), self.name)
        self.parent = None

    @property
    def display_name(self):
        return f'{self.name} ({self.contents_weight:.2f}/{self.capacity:.2f}):'

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
    def _check_search(itm: Item, **kwargs) -> bool:
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

    def check_add(self, weight: float) -> bool:
        """
        Recursively checks if weight can be added to a container and it parent
        container(s).

        :param weight: Weight to be added.
        :return: True/False if the weight can be added.
        """
        if self.contents_weight + weight > self.capacity:
            return False
        if self.parent is not None:
            return self.parent.check_add(weight)
        return True

    def add(self, *collections) -> tuple:
        """
        Adds collections to the container.

        :param collections: Collections or Container to add.
        :return: Tuple of collections that couldn't be added.
        """
        for i, coll in enumerate(collections):
            if not (isinstance(coll, Collection) or isinstance(coll, Container)):
                raise TypeError("collection at {i} is not a Collection or Container".format(i=i))

            if not self.check_add(coll.weight):
                return collections[i:]

            if isinstance(coll, Collection):
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

    def to_dict(self) -> dict:
        """
        Returns the container as a dictionary mapping.

        :return: Dictionary.
        """
        self.update()

        out = {
            'type': type(self).__name__,
            'name': self.name,
            'capacity': self.capacity,
            'weight': self.weight,
            'value': self.value,
            'contents': {key: val.to_dict() for key, val in self.contents.items()}
        }

        return out

    def __str__(self, offset='\t') -> str:
        s = self.display_name
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
        MagicItem.__init__(
            self,
            name=name,
            magic=magic,
            weight=weight,
            value=value,
            category=ItemCategory.CONTAINER,
            dmg=dmg
        )

        self.id = self._gen_id(
            unique_id or str(random.getrandbits(40)), str(self.category), self.name, self.magic
        )

    @property
    def display_name(self):
        return f'{self.name} {self.magic} ({self.contents_weight}/{self.capacity}):'

    @property
    def total_weight(self) -> float:
        """Returns total weight of container and its contents."""
        return self.weight

    def to_dict(self) -> dict:
        """
        Returns the container as a dictionary mapping.

        :return: Dictionary.
        """
        self.update()

        out = {
            'type': type(self).__name__,
            'name': self.name,
            'magic': self.magic,
            'capacity': self.capacity,
            'weight': self.weight,
            'value': self.value,
            'dmg': self.dmg,
            'contents': {key: val.to_dict() for key, val in self.contents.items()}
        }

        return out


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
        super(Player, self).__init__(
            name='player', capacity=capacity, weight=0.0, value=0.0, unique_id=name
        )
        self.player_name = name

    @property
    def display_name(self):
        return f'{self.player_name} ({self.contents_weight}/{self.capacity}):'

    @property
    def inventory(self) -> dict:
        return self.contents

    def to_dict(self) -> dict:
        """
        Returns the container as a dictionary mapping.

        :return: Dictionary.
        """
        self.update()

        out = {
            'type': type(self).__name__,
            'name': self.player_name,
            'capacity': self.capacity,
            'contents': {key: val.to_dict() for key, val in self.contents.items()}
        }

        return out


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

    def check_add(self, weight: float) -> bool:
        """
        Recursively checks if weight can be added to a container and it parent
        container(s).

        :param weight: Weight to be added.
        :return: True/False if the weight can be added.
        """
        return True

    def update(self):
        """
        Updates the current_weight, value, and weight properties
        as items are added to the container.
        """
        super(Store, self).update()
        self.capacity = self.contents_weight

    def to_dict(self) -> dict:
        """
        Returns the container as a dictionary mapping.

        :return: Dictionary.
        """
        self.update()

        out = {
            'type': type(self).__name__,
            'name': self.name,
            'contents': {key: val.to_dict() for key, val in self.contents.items()}
        }

        return out
