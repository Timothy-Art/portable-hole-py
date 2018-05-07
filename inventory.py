#!/usr/bin/env python3.6
import container


class Inventory(container.Container):
    """
    A Container representing an entire inventory.
    """
    def __init__(self):
        """
        Creates a new Inventory.
        """
        super(Inventory, self).__init__(name='Inventory', capacity=0)

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
            assert isinstance(con, container.Container), TypeError("collection at {i} is not a Container".format(i=i))

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
