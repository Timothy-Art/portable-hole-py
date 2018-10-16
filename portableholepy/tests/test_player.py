import random

from portableholepy import item, collection, container

random.seed(0)


class TestPlayer:
    @staticmethod
    def _build_container():
        new_item = item.Item(name='Sword', weight=5.0, value=10.0, category='weapon')
        new_magicitem = item.MagicItem(name='Sword', magic='+1', weight=5.0, value=10.0, category='weapon')
        new_coll = collection.Collection(itm=new_item, quantity=5)
        new_magiccoll = collection.Collection(itm=new_magicitem)

        new_con = container.Player(name='Player', capacity=200.0)
        new_con.add(new_coll)
        new_con.add(new_magiccoll)

        return new_con

    def test_creation(self):
        new_con = container.Player(name='Player', capacity=200.0)

        assert new_con.player_name == 'Player', 'Name is incorrect.'
        assert new_con.id == 'Player|container|player', 'ID is incorrectly generated.'

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

