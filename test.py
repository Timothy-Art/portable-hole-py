#!/usr/bin/env python3.6
import portablehole.items
from portablehole import inventory, items


inv = inventory.Inventory()
tim = portablehole.items.Player(name="Tim", capacity=135)
franklin = portablehole.items.Player(name="Franklin", capacity=160)
gp = portablehole.items.Collection(
    item=items.Item(name='GP', weight=0.01, value=1, category=items.ItemCategory.COIN))

inv.add(
    tim,
    franklin,
    portablehole.items.Store(name="Bank")
)

bank = next(inv.search(name="Bank"))

inv.add(franklin)

bank.add(gp*100)

coins = next(bank.search(id=f'{items.ItemCategory.COIN}|GP'))
coins.sub(20)
coins -= 5

coins.add(5)
coins += 15

coins.mult(2)
coins *= 2

coins = coins - 5
coins = coins + 5
coins = coins * 2
# print(coins)

arrows = portablehole.items.Collection(
    item=items.Item(name='Arrow', weight=0.1, value=0.1, category=items.ItemCategory.AMMUNITION),
    quantity=10
)
sword = portablehole.items.Collection(
    item=items.MagicItem(
        name="Sword", magic="+1", weight=2, value=10, category=items.ItemCategory.WEAPON
    )
)
bow = portablehole.items.Collection(
    item=items.Item(name="Longbow", weight=2, value=25, category=items.ItemCategory.WEAPON))
quiver = portablehole.items.Container(name="Quiver", capacity=4, weight=2, value=1)
backpack = portablehole.items.Container(name='Backpack', capacity=20, weight=5, value=2)
bag_o_holding = portablehole.items.MagicContainer(name="Bag of Holding", magic="250 lbs", capacity=250)

tim.add(backpack)
tim.add(quiver)
tim.add(sword)

tim_bp = next(tim.search(name="Backpack"))
tim_bp.add(bow)
tim_bp.add(sword)

quiver.add(arrows, arrows)

franklin.add(bag_o_holding)

bag_o_holding.add(sword*4)
bag_o_holding.add(gp*1000)
bag_o_holding.add(gp*1000)

search = inv.search(m=True)

for i in search:
    if i.parent:
        print(i.parent.id)
    print(i.id)

inv.update()
print(inv)
