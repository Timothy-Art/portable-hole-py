import random
import sys

from portablehole import item, collection, container

random.seed(0)


class TestStore:
    @staticmethod
    def _build_container():
        new_item = item.Item(name='Sword', weight=5.0, value=10.0, category='weapon')
        new_magicitem = item.MagicItem(name='Sword', magic='+1', weight=5.0, value=10.0, category='weapon')
        new_coll = collection.Collection(itm=new_item, quantity=5)
        new_magiccoll = collection.Collection(itm=new_magicitem)

        new_con = container.Store(name='Store')
        new_con.add(new_coll)
        new_con.add(new_magiccoll)

        return new_con

    def test_full(self):
        new_con = self._build_container()

        assert not new_con.full, 'Store cannot be full.'

    def test_add(self):
        new_con = self._build_container()
        add_item = item.Item(name="test", weight=1.0)
        add_coll = collection.Collection(itm=add_item)
        add_con = container.Container(name="Bag", capacity=5.0, weight=10.0)
        con_id = add_con.id

        try:
            new_con.add(add_item)
            raise AssertionError('Store should only accept Collection or Container types')
        except TypeError:
            pass
        except:
            print("Unexpected error", sys.exc_info()[0])
            raise

        assert new_con.capacity == 30.0, 'Capacity should match contents_weight'

        new_con.add(add_coll)
        add_coll += 2

        assert 'misc|test' in new_con.contents, 'Collection was not added.'
        assert new_con.capacity == 31.0, 'Capacity should update on add.'
        assert new_con.contents['misc|test'].quantity == 1, 'Collection was not copied to store.'

        new_con.add(add_con)

        assert con_id in new_con.contents, 'Container was not added.'
        assert new_con.capacity == 41.0, 'Capacity should update on add.'

        new_con.add(add_coll, add_coll)

        assert new_con.contents['misc|test'].quantity == 7, 'Same collections are not cumulated.'

        add_con.add(add_coll)

    def test_to_dict(self):
        new_con = self._build_container()

        d = new_con.to_dict()

        assert isinstance(d, dict), 'to_dict method doesn\'t return a dict.'
        assert 'contents' in d, 'item key missing.'
        assert isinstance(d['contents'], dict), 'contents was not converted to dict.'
        assert 'type' in d and d['type'] == 'Store', 'type key is incorrect.'
        assert 'name' in d, 'name key missing.'
