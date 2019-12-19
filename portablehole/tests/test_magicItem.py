import unittest

from portablehole import items


class TestMagicItem(unittest.TestCase):
    def test_creation(self):
        new_item = items.MagicItem(
            name='Sword', magic='+1', weight=5.0, value=10.0, category=items.ItemCategory.WEAPON, dmg=125
        )

        assert new_item.name == 'Sword', 'Name is incorrect.'
        assert new_item.magic == '+1', 'Magic is incorrect'
        assert new_item.category == items.ItemCategory.WEAPON, 'Category is incorrect.'
        assert new_item.m, 'Item should have m set to True.'
        assert isinstance(new_item.weight, float) and new_item.weight == 5.0, 'Weight is incorrect.'
        assert isinstance(new_item.value, float) and new_item.value == 10.0, 'Weight is incorrect.'
        assert new_item.id == f'{items.ItemCategory.WEAPON}|Sword|+1', 'ID is incorrectly generated.'

    def test_to_dict(self):
        new_item = items.MagicItem(
            name='Sword', magic='+1', weight=5.0, value=10.0, category=items.ItemCategory.WEAPON, dmg=125
        )

        d = new_item.to_dict()

        assert isinstance(d, dict), 'to_dict method doesn\'t return a dict.'
        assert 'name' in d, 'name key missing.'
        assert 'magic' in d, 'magic key missing.'
        assert 'category' in d, 'category key missing.'
        assert 'weight' in d, 'weight key missing.'
        assert 'value' in d, 'value key missing.'
        assert 'dmg' in d, 'dmg key missing.'
        assert 'type' in d and d['type'] == 'MagicItem', 'type key is incorrect.'

    def test_str(self):
        new_item = items.MagicItem(
            name='Sword', magic='+1', weight=5.0, value=10.0, category=items.ItemCategory.WEAPON
        )

        assert str(new_item) == 'Sword +1', '__str__ for MagicItem should return its name followed by its magic.'
