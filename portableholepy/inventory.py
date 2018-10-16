from portableholepy import collection, container, item


class Inventory(container.Store):
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

    def add(self, *containers: container.Container):
        """
        Adds containers to the inventory.

        :param containers: Containers to add.
        """
        for i, con in enumerate(containers):
            if not isinstance(con, container.Container):
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


def from_dict(inventory):
    """
    Generates an Inventory from a dictionary.

    :param inventory: Dictionary of inventory.
    :return: Inventory
    """
    inv = Inventory()
    if inventory['type'] == 'Inventory':
        inventory = inventory['contents']

    def _rec_dict(d):
        if d['type'] == 'Item':
            return item.Item(
                name=d['name'],
                weight=d['weight'],
                value=d['value'],
                category=d['category']
            )
        elif d['type'] == 'MagicItem':
            return item.MagicItem(
                name=d['name'],
                magic=d['magic'],
                weight=d['weight'],
                value=d['value'],
                category=d['category'],
                dmg=d['dmg']
            )
        elif d['type'] == 'Collection':
            return collection.Collection(
                itm=_rec_dict(d['item']),
                quantity=d['quantity']
            )
        elif d['type'] == 'Container':
            out = container.Container(
                name=d['name'],
                capacity=d['capacity'],
                weight=d['weight'],
                value=d['value']
            )
            for j in d['contents'].values():
                out.add(_rec_dict(j))
            return out
        elif d['type'] == 'MagicContainer':
            out = container.MagicContainer(
                name=d['name'],
                magic=d['magic'],
                capacity=d['capacity'],
                weight=d['weight'],
                value=d['value'],
                dmg=d['dmg']
            )
            for j in d['contents'].values():
                out.add(_rec_dict(j))
            return out
        elif d['type'] == 'Player':
            out = container.Player(
                name=d['name'],
                capacity=d['capacity'],
            )
            for j in d['contents'].values():
                out.add(_rec_dict(j))
            return out
        elif d['type'] == 'Store':
            out = container.Store(
                name=d['name']
            )
            for j in d['contents'].values():
                out.add(_rec_dict(j))
            return out

    for i in inventory.values():
        inv.add(_rec_dict(i))

    return inv
