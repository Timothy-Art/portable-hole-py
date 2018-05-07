#!/usr/bin/env python3.6
import item


class Collection:
    """
    A collection of Items
    """
    def __init__(self, itm: item.Item, quantity: int = 1):
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
        self.parent = None

    def add(self, n: int=1):
        """
        Adds to the Collection.

        :param n: Quantity to add.
        """
        try:
            n = int(n)
        except ValueError:
            raise TypeError("unsupported operand type for add: {other}".format(other=type(n)))

        assert self.quantity + n >= 0, ValueError("quantity cannot be < 0")
        self.quantity += n
        self.weight += n * self.item.weight
        self.value += n * self.item.value

    def __add__(self, other: int):
        try:
            other = int(other)
        except ValueError:
            raise TypeError("unsupported operand type for +: {other}".format(other=type(other)))

        assert self.quantity + other >= 0, ValueError("quantity cannot be < 0")
        self.quantity += other
        self.weight += other * self.item.weight
        self.value += other * self.item.value
        return self

    def __iadd__(self, other: int):
        try:
            other = int(other)
        except ValueError:
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
        except ValueError:
            raise TypeError("unsupported operand type for sub: {other}".format(other=type(n)))

        assert self.quantity - n >= 0, ValueError("quantity cannot be < 0")
        self.quantity -= n
        self.weight -= n * self.item.weight
        self.value -= n * self.item.value

    def __sub__(self, other: int):
        try:
            other = int(other)
        except ValueError:
            raise TypeError("unsupported operand type for -: {other}".format(other=type(other)))

        assert self.quantity + other >= 0, ValueError("quantity cannot be < 0")
        self.quantity -= other
        self.weight -= other * self.item.weight
        self.value -= other * self.item.value
        return self

    def __isub__(self, other: int):
        try:
            other = int(other)
        except ValueError:
            raise TypeError("unsupported operand type for -=: {other}".format(other=type(other)))

        assert self.quantity + other >= 0, ValueError("quantity cannot be < 0")
        self.quantity -= other
        self.weight -= other * self.item.weight
        self.value -= other * self.item.value
        return self

    def __str__(self) -> str:
        return f'{self.item}  x{self.quantity}'

    def __copy__(self):
        return Collection(self.item, quantity=self.quantity)
