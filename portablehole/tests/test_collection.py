import unittest
from copy import copy

import portablehole.items


class TestCollection(unittest.TestCase):
    def test_creation(self):
        new_item = portablehole.items.Item(
            name='Sword', weight=5.0, value=10.0, category=portablehole.items.ItemCategory.WEAPON
        )
        new_magicitem = portablehole.items.MagicItem(
            name='Sword', magic='+1', weight=5.0,
            value=10.0, category=portablehole.items.ItemCategory.WEAPON
        )
        new_coll = portablehole.items.Collection(item=new_item, quantity=5)
        new_magiccoll = portablehole.items.Collection(item=new_magicitem)

        assert new_coll.name == 'Sword', 'Name is incorrect.'
        assert new_coll.category == portablehole.items.ItemCategory.WEAPON, 'Category is incorrect.'
        assert isinstance(new_coll.quantity, int) and new_coll.quantity == 5, 'Quantity is incorrect.'
        assert isinstance(new_coll.weight, float) and new_coll.weight == 5.0*5, 'Weight is incorrect.'
        assert isinstance(new_coll.value, float) and new_coll.value == 10.0*5, 'Weight is incorrect.'
        assert new_coll.id == f'{portablehole.items.ItemCategory.WEAPON}|Sword', (
            'ID is incorrectly generated.'
        )

        assert new_coll.item.parent == new_coll, 'Parent of item not being set.'
        assert new_coll.item == new_item, 'Item not being set correctly.'

        assert not new_coll.m, 'Collection should not have m set to True.'
        assert new_magiccoll.m, 'Collection of MagicItem should have m set to True.'
        assert new_coll.magic is None, 'Collection magic is incorrect.'
        assert new_magiccoll.magic == '+1', 'Collection magic is incorrect.'

    def test_to_dict(self):
        new_item = portablehole.items.Item(name='Sword', weight=5.0, value=10.0, category='weapon')
        new_coll = portablehole.items.Collection(item=new_item, quantity=5)

        d = new_coll.to_dict()

        assert isinstance(d, dict), 'to_dict method doesn\'t return a dict.'
        assert 'item' in d, 'item key missing.'
        assert isinstance(d['item'], dict), 'item was not converted to dict.'
        assert 'quantity' in d, 'quantity key missing.'
        assert 'type' in d and d['type'] == 'Collection', 'type key is incorrect.'

    def test_str(self):
        new_item = portablehole.items.Item(name='Sword', weight=5.0, value=10.0, category='weapon')
        new_coll = portablehole.items.Collection(item=new_item, quantity=5)

        assert str(new_coll) == 'Sword  x5', (
            '__str__ for Collection should return item string followed by quantity.'
        )

    def test_eq(self):
        item_a = portablehole.items.Item(name='Sword', weight=5.0, value=10.0, category='weapon')
        item_b = portablehole.items.Item(name='Bow', weight=5.0, value=10.0, category='weapon')

        coll_a = portablehole.items.Collection(item=item_a, quantity=5)
        coll_b = portablehole.items.Collection(item=item_a, quantity=5)
        coll_c = portablehole.items.Collection(item=item_a, quantity=10)
        coll_d = portablehole.items.Collection(item=item_b, quantity=5)

        assert coll_a == coll_b, 'Same collections return False'
        assert coll_a != coll_c, 'Different collections return True'
        assert coll_a != coll_d, 'Collections with different items return True.'

    def test_add(self):
        new_item = portablehole.items.Item(name='Sword', weight=5.0, value=10.0, category='weapon')
        new_coll = portablehole.items.Collection(item=new_item, quantity=5)

        assert new_coll.quantity == 5, 'Initial quantity is wrong.'

        new_coll.add(10)

        assert new_coll.quantity == 15, 'add method fails to update quantity.'
        assert new_coll.weight == 5 * 15, 'Weight incorrectly updated on add.'
        assert new_coll.value == 10 * 15, 'Value incorrectly updated on add.'

        try:
            new_coll.add(new_coll)
            raise AssertionError('Addition of non-numeric should raise a TypeError.')
        except TypeError:
            pass

        new_coll += 5

        assert new_coll.quantity == 20, '__iadd__ method fails to update quantity.'
        assert new_coll.weight == 5 * 20, 'Weight incorrectly updated on __iadd__.'
        assert new_coll.value == 10 * 20, 'Value incorrectly updated on __iadd__.'

        try:
            new_coll += new_coll
            raise AssertionError('Addition of non-numeric should raise a TypeError.')
        except TypeError:
            pass

        add_coll = new_coll + 5

        assert new_coll.quantity == 20, '__add__ method updates quantity.'
        assert new_coll.weight == 5 * 20, 'Weight incorrectly updates on __add__.'
        assert new_coll.value == 10 * 20, 'Value incorrectly updates on __add__.'

        assert isinstance(add_coll, portablehole.items.Collection), '__add__ should return a Collection.'
        assert add_coll.quantity == 25, '__add__ method fails to update quantity.'
        assert add_coll.weight == 5 * 25, 'Weight incorrectly updated on __add__.'
        assert add_coll.value == 10 * 25, 'Value incorrectly updated on __add__.'

        try:
            add_coll = new_coll + new_coll
            raise AssertionError('Addition of non-numeric should raise a TypeError.')
        except TypeError:
            pass

    def test_sub(self):
        new_item = portablehole.items.Item(name='Sword', weight=5.0, value=10.0, category='weapon')
        new_coll = portablehole.items.Collection(item=new_item, quantity=25)

        assert new_coll.quantity == 25, 'Initial quantity is wrong.'

        new_coll.sub(10)

        assert new_coll.quantity == 15, 'sub method fails to update quantity.'
        assert new_coll.weight == 5 * 15, 'Weight incorrectly updated on sub.'
        assert new_coll.value == 10 * 15, 'Value incorrectly updated on sub.'

        try:
            new_coll.sub(new_coll)
            raise AssertionError('Subtraction of non-numeric should raise a TypeError.')
        except TypeError:
            pass

        new_coll -= 5

        assert new_coll.quantity == 10, '__isub__ method fails to update quantity.'
        assert new_coll.weight == 5 * 10, 'Weight incorrectly updated on __isub__.'
        assert new_coll.value == 10 * 10, 'Value incorrectly updated on __isub__.'

        try:
            new_coll -= new_coll
            raise AssertionError('Subtraction of non-numeric should raise a TypeError.')
        except TypeError:
            pass

        sub_coll = new_coll - 5

        assert new_coll.quantity == 10, '__sub__ method updates quantity.'
        assert new_coll.weight == 5 * 10, 'Weight incorrectly updates on __sub__.'
        assert new_coll.value == 10 * 10, 'Value incorrectly updates on __sub__.'

        assert isinstance(sub_coll, portablehole.items.Collection), '__sub__ should return a Collection.'
        assert sub_coll.quantity == 5, '__sub__ method fails to update quantity.'
        assert sub_coll.weight == 5 * 5, 'Weight incorrectly updated on __sub__.'
        assert sub_coll.value == 10 * 5, 'Value incorrectly updated on __sub__.'

        try:
            sub_coll = new_coll - new_coll
            raise AssertionError('Subtraction of non-numeric should raise a TypeError.')
        except TypeError:
            pass

    def test_mult(self):
        new_item = portablehole.items.Item(name='Sword', weight=5.0, value=10.0, category='weapon')
        new_coll = portablehole.items.Collection(item=new_item)

        assert new_coll.quantity == 1, 'Initial quantity is wrong.'

        new_coll.mult(2)

        assert new_coll.quantity == 2, 'mult method fails to update quantity.'
        assert new_coll.weight == 5 * 2, 'Weight incorrectly updated on mult.'
        assert new_coll.value == 10 * 2, 'Value incorrectly updated on mult.'

        try:
            new_coll.mult(new_coll)
            raise AssertionError('Multiplication of non-numeric should raise a TypeError.')
        except TypeError:
            pass

        new_coll *= 5

        assert new_coll.quantity == 10, '__imul__ method fails to update quantity.'
        assert new_coll.weight == 5 * 10, 'Weight incorrectly updated on __imul__.'
        assert new_coll.value == 10 * 10, 'Value incorrectly updated on __imul__.'

        try:
            new_coll *= new_coll
            raise AssertionError('Multiplication of non-numeric should raise a TypeError.')
        except TypeError:
            pass

        mul_coll = new_coll * 2

        assert new_coll.quantity == 10, '__mul__ method updates quantity.'
        assert new_coll.weight == 5 * 10, 'Weight incorrectly updates on __mul__.'
        assert new_coll.value == 10 * 10, 'Value incorrectly updates on __mul__.'

        assert isinstance(mul_coll, portablehole.items.Collection), '__mul__ should return a Collection.'
        assert mul_coll.quantity == 20, '__mul__ method fails to update quantity.'
        assert mul_coll.weight == 5 * 20, 'Weight incorrectly updated on __mul__.'
        assert mul_coll.value == 10 * 20, 'Value incorrectly updated on __mul__.'

        try:
            mul_coll = new_coll * new_coll
            raise AssertionError('Multiplication of non-numeric should raise a TypeError.')
        except TypeError:
            pass

    def test_copy(self):
        new_item = portablehole.items.Item(name='Sword', weight=5.0, value=10.0, category='weapon')
        new_coll = portablehole.items.Collection(item=new_item, quantity=5)

        copied = copy(new_coll)

        assert copied == new_coll, 'Copy is not the same.'
