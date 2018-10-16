import random
import sys

from portableholepy import item, collection, container

random.seed(0)


class TestContainer:
    @staticmethod
    def _build_container():
        new_item = item.Item(name='Sword', weight=5.0, value=10.0, category='weapon')
        new_magicitem = item.MagicItem(name='Sword', magic='+1', weight=5.0, value=10.0, category='weapon')
        new_coll = collection.Collection(itm=new_item, quantity=5)
        new_magiccoll = collection.Collection(itm=new_magicitem)

        new_con = container.Container(name='Bag', capacity=200.0, weight=10.0, value=15.0)
        new_con.add(new_coll)
        new_con.add(new_magiccoll)

        return new_con

    def test_creation(self):
        new_con = container.Container(name='Bag', capacity=200.0, weight=10.0, value=15.0)

        assert new_con.name == 'Bag', 'Name is incorrect.'
        assert new_con.category == 'container', 'Category is incorrect.'
        assert new_con.id == '424533559245|container|Bag', 'ID is incorrectly generated.'
        assert new_con.capacity == 200.0, 'Capacity is incorrect.'
        assert new_con.contents_weight == 0.0, 'Contents weight is incorrect.'
        assert new_con.contents_value == 0.0, 'Contents value is incorrect.'
        assert isinstance(new_con.contents, dict), 'Contents is not a dictionary.'
        assert len(new_con.contents) == 0, 'Contents is not initialized correctly.'

    def test_full(self):
        new_con = self._build_container()

        assert not new_con.full, 'Container should not be full.'

        fill = collection.Collection(itm=item.Item(name='fill', weight=200.0-30.0, value=1.0))
        new_con.add(fill)

        assert new_con.full, 'Container should be full.'

    def test_free(self):
        new_con = self._build_container()

        assert new_con.free == 170.0, 'free property is not calculated correctly.'

    def test_total_weight(self):
        new_con = self._build_container()

        assert new_con.total_weight == 40.0, 'total_weight property is not calculated correctly.'

    def test_total_value(self):
        new_con = self._build_container()

        assert new_con.total_value == 75.0, 'total_weight property is not calculated correctly.'

    def test_add(self):
        new_con = self._build_container()
        add_item = item.Item(name="test", weight=1.0)
        add_coll = collection.Collection(itm=add_item)
        add_con = container.Container(name="Bag", capacity=5.0)
        add_fill = collection.Collection(itm=add_item, quantity=200)
        con_id = add_con.id

        try:
            new_con.add(add_item)
            raise AssertionError('Container should only accept Collection or Container types')
        except TypeError:
            pass
        except:
            print("Unexpected error", sys.exc_info()[0])
            raise

        new_con.add(add_coll)
        add_coll += 2

        assert 'misc|test' in new_con.contents, 'Collection was not added.'
        assert new_con.contents['misc|test'].quantity == 1, 'Collection was not copied to container.'

        new_con.add(add_con)

        assert con_id in new_con.contents, 'Container was not added.'

        new_con.add(add_coll, add_coll)

        assert new_con.contents['misc|test'].quantity == 7, 'Same collections are not cumulated.'

        full = new_con.add(add_fill)

        assert isinstance(full, tuple) and len(full) == 1, 'Full container should return tuple of items not added.'
        assert full[0] == add_fill, 'Container accepted collection that would cause overflow.'

    def test_sub(self):
        new_con = self._build_container()

        test = new_con.sub('weapon|Sword')

        assert 'weapon|Sword' not in new_con.contents, 'Collection was not subtracted.'
        assert test, 'sub method should return true if collection was subtracted.'

        test = new_con.sub('misc|test')

        assert not test, 'sub method should return false if collection wasn\'t subtracted'

    def test_search(self):
        new_con = self._build_container()
        sub_con = self._build_container()

        new_con.add(sub_con)

        collections = [coll for coll in new_con.search(name='Sword')]

        assert len(collections) == 4, 'Search did not find all collections.'
        for coll in collections:
            assert coll.name == 'Sword', 'Search found collections without the criteria.'

        magic_collections = [coll for coll in new_con.search(name='Sword', m=True)]

        assert len(magic_collections) == 2, 'Search did not find all collections.'
        for coll in magic_collections:
            assert coll.name == 'Sword', 'Search found collections without all criteria.'

    def test_to_dict(self):
        new_con = self._build_container()
        d = new_con.to_dict()

        assert isinstance(d, dict), 'to_dict method doesn\'t return a dict.'
        assert 'contents' in d, 'item key missing.'
        assert isinstance(d['contents'], dict), 'contents was not converted to dict.'
        assert 'type' in d and d['type'] == 'Container', 'type key is incorrect.'
        assert 'name' in d, 'name key missing.'
        assert 'capacity' in d, 'capacity key missing.'
        assert 'weight' in d, 'weight key missing.'
        assert 'value' in d, 'value key missing.'
