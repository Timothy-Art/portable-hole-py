import unittest

import portablehole.items


class TestItem(unittest.TestCase):
    def test_creation(self):
        new_item = portablehole.items.Item(
            name='Sword', weight=5.0, value=10.0, category=portablehole.items.ItemCategory.WEAPON
        )

        assert new_item.name == 'Sword', 'Name is incorrect.'
        assert new_item.category == portablehole.items.ItemCategory.WEAPON, 'Category is incorrect.'
        assert not new_item.m, 'Item should not have m set to True.'
        assert isinstance(new_item.weight, float) and new_item.weight == 5.0, 'Weight is incorrect.'
        assert isinstance(new_item.value, float) and new_item.value == 10.0, 'Weight is incorrect.'
        assert new_item.id == f'{portablehole.items.ItemCategory.WEAPON}|Sword', (
            'ID is incorrectly generated.'
        )

    def test_to_dict(self):
        new_item = portablehole.items.Item(
            name='Sword', weight=5.0, value=10.0, category=portablehole.items.ItemCategory.WEAPON
        )

        d = new_item.to_dict()

        assert isinstance(d, dict), 'to_dict method doesn\'t return a dict.'
        assert 'name' in d, 'name key missing.'
        assert 'category' in d, 'category key missing.'
        assert 'weight' in d, 'weight key missing.'
        assert 'value' in d, 'value key missing.'
        assert 'type' in d and d['type'] == 'Item', 'type key is incorrect.'

    def test_str(self):
        new_item = portablehole.items.Item(
            name='Sword', weight=5.0, value=10.0, category=portablehole.items.ItemCategory.WEAPON
        )

        assert str(new_item) == new_item.name, '__str__ for Item should return its name.'

    def test_eq(self):
        item_a = portablehole.items.Item(
            name='Sword', weight=5.0, value=10.0, category=portablehole.items.ItemCategory.WEAPON
        )
        item_b = portablehole.items.Item(
            name='Sword', weight=5.0, value=10.0, category=portablehole.items.ItemCategory.WEAPON
        )
        item_c = portablehole.items.Item(
            name='Bow', weight=10.0, value=20.0, category=portablehole.items.ItemCategory.WEAPON
        )
        item_d = portablehole.items.Item(
            name='Sword', weight=5.0, value=15.0, category=portablehole.items.ItemCategory.WEAPON
        )
        item_e = portablehole.items.Item(
            name='Sword', weight=10.0, value=10.0, category=portablehole.items.ItemCategory.WEAPON
        )

        assert item_a == item_b, 'Same items return False.'
        assert item_a != item_d, 'Same item name with differing value return True'
        assert item_a != item_e, 'Same item name with differing weight return True'
        assert item_a != item_c, 'Different items return True.'
