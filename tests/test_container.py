import random

from portablehole import item, collection, container

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
        pass

    def test_sub(self):
        pass

    def test_search(self):
        pass

    def test_to_dict(self):
        new_con = self._build_container()

        d = new_con.to_dict()

        assert isinstance(d, dict), 'to_dict method doesn\'t return a dict.'
        assert 'contents' in d, 'item key missing.'
        assert isinstance(d['contents'], dict), 'contents was not converted to dict.'
        assert 'type' in d and d['type'] == 'Container', 'type key is incorrect.'
        assert 'name' in d, 'name key missing.'
        assert 'weight' in d, 'weight key missing.'
        assert 'value' in d, 'value key missing.'
