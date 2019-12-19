from portablehole import items


class Inventory(items.Store):
    """
    A Container representing an entire inventory.
    """
    def __init__(self):
        """
        Creates a new Inventory.
        """
        super(Inventory, self).__init__(name='Inventory')

    def update(self):
        """
        Updates the current_weight, value, and weight properties
        as items are added to the container.
        """
        contents_weight = 0
        contents_value = 0
        capacity = 0

        for key in self.contents:
            self.contents[key].update()
            capacity += self.contents[key].capacity
            contents_weight += self.contents[key].total_weight
            contents_value += self.contents[key].total_value

        self.contents_weight = contents_weight
        self.contents_value = contents_value
        self.capacity = capacity

    def add(self, *containers: items.Container):
        """
        Adds containers to the inventory.

        :param containers: Containers to add.
        """
        for i, con in enumerate(containers):
            if not isinstance(con, items.Container):
                raise TypeError("collection at {i} is not a Container".format(i=i))

            self.contents[con.id] = con
            self.update()

    def sub(self, container_id: str) -> bool:
        """
        Subtracts a container from the Inventory.

        :param container_id: Container ID to remove.
        :return: True/False if the container was subtracted.
        """
        if container_id in self.contents:
            del self.contents[container_id]
            self.update()
            return True
        return False

    @staticmethod
    def _check_search(itm: items.Item, **kwargs) -> bool:
        """
        Checks if an item matches the search conditions.

        :param kwargs: Properties to check.
        :return: True/False
        """
        for key, val in kwargs.items():
            if not hasattr(itm, key):
                return False
            if getattr(itm, key) != val:
                return False
        return True

    def sub_inventory(self, **kwargs):
        sub_inv = self.to_dict()

        for key in self.contents:
            if self._check_search(self.contents[key], **kwargs):
                yield self.contents[key]
            if isinstance(self.contents[key], items.Container):
                for i in self.contents[key].search(**kwargs):
                    yield i

        return Inventory.from_dict(sub_inv)

    def to_dict(self) -> dict:
        """
        Returns the container as a dictionary mapping.

        :return: Dictionary.
        """
        self.update()
        out = {
            'type':     type(self).__name__,
            'name':     self.name,
            'contents': {key: val.to_dict() for key, val in self.contents.items()}
        }

        return out

    @staticmethod
    def _from_dict(d):
        if d['type'] == 'Item':
            return items.Item(
                name=d['name'],
                weight=d['weight'],
                value=d['value'],
                category=d['category']
            )
        elif d['type'] == 'MagicItem':
            return items.MagicItem(
                name=d['name'],
                magic=d['magic'],
                weight=d['weight'],
                value=d['value'],
                category=d['category'],
                dmg=d['dmg']
            )
        elif d['type'] == 'Collection':
            return items.Collection(item=Inventory._from_dict(d['item']), quantity=d['quantity'])
        elif d['type'] == 'Container':
            out = items.Container(
                name=d['name'],
                capacity=d['capacity'],
                weight=d['weight'],
                value=d['value']
            )
            for j in d['contents'].values():
                out.add(Inventory._from_dict(j))
            return out
        elif d['type'] == 'MagicContainer':
            out = items.MagicContainer(
                name=d['name'],
                magic=d['magic'],
                capacity=d['capacity'],
                weight=d['weight'],
                value=d['value'],
                dmg=d['dmg']
            )
            for j in d['contents'].values():
                out.add(Inventory._from_dict(j))
            return out
        elif d['type'] == 'Player':
            out = items.Player(
                name=d['name'],
                capacity=d['capacity'],
            )
            for j in d['contents'].values():
                out.add(Inventory._from_dict(j))
            return out
        elif d['type'] == 'Store':
            out = items.Store(
                name=d['name']
            )
            for j in d['contents'].values():
                out.add(Inventory._from_dict(j))
            return out

    @staticmethod
    def from_dict(inventory):
        """
        Generates an Inventory from a dictionary.

        :param inventory: Dictionary of inventory.
        :return: Inventory
        """
        inv = Inventory()
        if inventory['type'] == 'Inventory':
            inventory = inventory['contents']

        for i in inventory.values():
            inv.add(Inventory._from_dict(i))

        return inv
