import random
import unittest

import portablehole.items
import portablehole.inventory

random.seed(0)


class TestInventory(unittest.TestCase):
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

        new_con = portablehole.items.Container(
            name='Bag', capacity=200.0, weight=10.0, value=15.0, unique_id='00'
        )
        new_con.add(new_coll)
        new_con.add(new_magiccoll)

        new_magiccon = portablehole.items.MagicContainer(
            name='Bag', magic='of Holding', capacity=250.0, weight=15.0
        )
        new_magiccon.add(new_coll)

        player = portablehole.items.Player(name="Player_1", capacity=300.0)
        store = portablehole.items.Store(name="Store")

        store.add(new_con)
        player.add(new_magiccon)

        inv = portablehole.inventory.Inventory()

        inv.add(store, player)

        return inv

    def test_add(self):
        new_con = self._build_container()
        add_item = portablehole.items.Item(name="test", weight=1.0)
        add_coll = portablehole.items.Collection(item=add_item)
        add_con = portablehole.items.Container(name="Bag", capacity=5.0)
        con_id = add_con.id

        try:
            new_con.add(add_coll)
            raise AssertionError('Inventory should only accept Container types')
        except TypeError:
            pass

        new_con.add(add_con)

        assert con_id in new_con.contents, 'Container was not added.'

    def test_sub(self):
        new_con = self._build_container()

        test = new_con.sub(f'Player_1|{portablehole.items.ItemCategory.CONTAINER}|player')

        assert f'Player_1|{portablehole.items.ItemCategory.CONTAINER}|player' not in new_con.contents, (
            'Container was not subtracted.'
        )
        assert test, 'sub method should return true if container was subtracted.'

        test = new_con.sub('misc|test')

        assert not test, 'sub method should return false if container wasn\'t subtracted'

    def test_to_dict(self):
        new_con = self._build_container()
        d = new_con.to_dict()

        assert isinstance(d, dict), 'to_dict method doesn\'t return a dict.'
        assert 'contents' in d, 'item key missing.'
        assert isinstance(d['contents'], dict), 'contents was not converted to dict.'
        assert 'type' in d and d['type'] == 'Inventory', 'type key is incorrect.'

    def test_from_dict(self):
        def _rec_assert(i):
            assert (
                isinstance(i, portablehole.items.Container) or isinstance(i, portablehole.items.Collection)
            ), (
                'Contents of Containers are not imported correctly'
            )
            if isinstance(i, portablehole.items.Collection):
                assert isinstance(i.item, portablehole.items.Item), (
                    'Collections are not imported correctly'
                )
            else:
                for j in i.contents.values():
                    _rec_assert(j)

        new_con = self._build_container()
        d = new_con.to_dict()

        test_con = portablehole.inventory.Inventory.from_dict(d)

        assert isinstance(test_con, portablehole.inventory.Inventory), (
            'from_dict should return an Inventory.'
        )
        assert len(test_con.contents) == len(new_con.contents), 'Contents were not all copied.'

        for con in test_con.contents.values():
            assert isinstance(con, portablehole.items.Container), 'Contents are not imported correctly'
            for itm in con.contents.values():
                _rec_assert(itm)
