import random
import unittest

import portablehole.items

random.seed(0)


class TestPlayer(unittest.TestCase):
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

        new_con = portablehole.items.Player(name='Player', capacity=200.0)
        new_con.add(new_coll)
        new_con.add(new_magiccoll)

        return new_con

    def test_creation(self):
        new_con = portablehole.items.Player(name='Player', capacity=200.0)

        assert new_con.player_name == 'Player', 'Name is incorrect.'
        assert new_con.id == f'Player|{portablehole.items.ItemCategory.CONTAINER}|player', (
            'ID is incorrectly generated.'
        )

    def test_inventory(self):
        new_con = self._build_container()

        assert new_con.contents == new_con.inventory, 'Inventory should be an alias for contents.'

    def test_to_dict(self):
        new_con = self._build_container()
        d = new_con.to_dict()

        assert isinstance(d, dict), 'to_dict method doesn\'t return a dict.'
        assert 'contents' in d, 'item key missing.'
        assert isinstance(d['contents'], dict), 'contents was not converted to dict.'
        assert 'type' in d and d['type'] == 'Player', 'type key is incorrect.'
        assert 'name' in d, 'name key missing.'
        assert 'capacity' in d, 'capacity key missing.'

