#!/usr/bin/env python3
from item import Item


class Container(Item):
    """
    A Container item that can hold other items. In addition to the standard item properties,
    it also has a weight allowance that it can hold.
    """

    def __init__(self, allowance, **kwargs):
        """
        Creates a new Container.

        :param allowance: Maximum weight that can be held.
        :param kwargs: Parameters to pass to the Item constructor.
        """

        self.allowance = allowance
        self.current_weight = 0
        self.storage = []
        super().__init__(**kwargs)
