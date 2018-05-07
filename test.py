#!/usr/bin/env python3.6
import item
import collection
import container
import inventory

inv = inventory.Inventory()

inv.add(
    container.Player(name="Tim", capacity=135),
    container.Player(name="Franklin", capacity=160),
    container.MagicContainer(name="Bag", magic="of Holding", capacity=250)
)

print(inv)

arrows = collection.Collection(itm=item.Item(name='Arrow', weight=0.1, value=0.1, category='ammunition'), quantity=10)
sword = collection.Collection(itm=item.MagicItem(name="Sword", magic="+1", weight=2, value=10, category='weapon'))
bow = collection.Collection(itm=item.Item(name="Longbow", weight=2, value=25, category='weapon'))
quiver = container.Container(name="Quiver", capacity=4, weight=2, value=1)
backpack = container.Container(name='Backpack', capacity=20, weight=5, value=2)

tim = next(inv.search(player_name="Tim"))
franklin = next(inv.search(player_name="Franklin"))

tim.add(backpack)
tim.add(quiver)
tim.add(sword)

tim_bp = next(tim.search(name="Backpack"))
tim_bp.add(bow)
tim_bp.add(sword)

quiver.add(arrows, arrows)

search = backpack.search(m=True)

franklin.add(backpack)

for i in search:
    print(i)

inv.update()
print(inv)
