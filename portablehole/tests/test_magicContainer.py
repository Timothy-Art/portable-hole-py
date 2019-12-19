import random
import unittest

import portablehole.items
random.seed(0)


class TestMagicContainer(unittest.TestCase):
    @staticmethod
    def _build_container():
        new_item = portablehole.items.Item(
            name='Sword', weight=5.0, value=10.0, category=portablehole.items.ItemCategory.WEAPON
        )
        new_magicitem = portablehole.items.MagicItem(
            name='Sword', magic='+1', weight=5.0,
            value=10.0, category=portablehole.items.ItemCategory.WEAPON
        )
        new_coll = portablehole.items.Collection(item=new_item, quantity=5)
        new_magiccoll = portablehole.items.Collection(item=new_magicitem)

        new_con = portablehole.items.MagicContainer(
            name='Bag', magic='of Holding', capacity=200.0, weight=10.0, value=15.0
        )
        new_con.add(new_coll)
        new_con.add(new_magiccoll)

        return new_con

    def test_creation(self):
        new_con = portablehole.items.MagicContainer(
            name='Bag', magic='of Holding', capacity=200.0, weight=10.0, value=15.0
        )

        assert new_con.name == 'Bag', 'Name is incorrect.'
        assert (
            new_con.id == f'1007378992806|{portablehole.items.ItemCategory.CONTAINER}|Bag|of Holding'
        ), (
            'ID is incorrectly generated.'
        )
        assert new_con.m, 'm property should be True.'
        assert new_con.magic == 'of Holding', 'Magic is incorrect'

    def test_total_weight(self):
        new_con = self._build_container()

        assert new_con.total_weight == new_con.weight, 'MagicContainer total_weight is not fixed.'

        new_con.sub(f'{portablehole.items.ItemCategory.WEAPON}|Sword')

        assert new_con.total_weight == new_con.weight, 'MagicContainer total_weight is not fixed.'

    def test_to_dict(self):
        new_con = self._build_container()
        d = new_con.to_dict()

        assert isinstance(d, dict), 'to_dict method doesn\'t return a dict.'
        assert 'contents' in d, 'item key missing.'
        assert isinstance(d['contents'], dict), 'contents was not converted to dict.'
        assert 'type' in d and d['type'] == 'MagicContainer', 'type key is incorrect.'
        assert 'name' in d, 'name key missing.'
        assert 'capacity' in d, 'capacity key missing.'
        assert 'weight' in d, 'weight key missing.'
        assert 'value' in d, 'value key missing.'
        assert 'magic' in d, 'magic key missing.'
        assert 'dmg' in d, 'dmg key missing.'
