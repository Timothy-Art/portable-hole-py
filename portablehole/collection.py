#!/usr/bin/env python3.6
class Collection:
    """
    A collection of Items
    """
    def __init__(self, itm, quantity: int = 1):
        """
        Creates a new Collection of a given Item.

        :param itm: Item to collect.
        :param quantity: Quantity of Items to start with. Defaults to 1.
        """
        self.item = itm
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

    def add(self, n: int=1):
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
        return Collection(itm=self.item, quantity=self.quantity + other)

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

    def sub(self, n: int=1):
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

        return Collection(itm=self.item, quantity=self.quantity - other)

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

    def mult(self, n: int=1):
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
        return Collection(itm=self.item, quantity=self.quantity * other)

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

    def __str__(self) -> str:
        return f'{self.item}  x{self.quantity}'

    def __copy__(self):
        return Collection(self.item, quantity=self.quantity)

    def __eq__(self, other):
        if not isinstance(other, Collection):
            return False
        if not other.item == self.item:
            return False
        if not other.quantity == self.quantity:
            return False
        return True
