#!/usr/bin/env python3.6
import item
import collection
import container
import inventory
import pprint

inv = inventory.Inventory()
tim = container.Player(name="Tim", capacity=135)
franklin = container.Player(name="Franklin", capacity=160)
gp = collection.Collection(itm=item.Item(name='GP', weight=0.01, value=1, category='coin'))

inv.add(
    tim,
    franklin,
    container.Store(name="Bank")
)

bank = next(inv.search(name="Bank"))

print(bank)
print(inv.sub('franklin'))
print(inv.sub(franklin.id))

print(inv)

inv.add(franklin)

bank.add(gp*100)

coins = next(bank.search(id='coin|GP'))
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

arrows = collection.Collection(itm=item.Item(name='Arrow', weight=0.1, value=0.1, category='ammunition'), quantity=10)
sword = collection.Collection(itm=item.MagicItem(name="Sword", magic="+1", weight=2, value=10, category='weapon'))
bow = collection.Collection(itm=item.Item(name="Longbow", weight=2, value=25, category='weapon'))
quiver = container.Container(name="Quiver", capacity=4, weight=2, value=1)
backpack = container.Container(name='Backpack', capacity=20, weight=5, value=2)
bag_o_holding = container.MagicContainer(name="Bag", magic="of Holding", capacity=250)

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
    print(i.name+i.magic)

inv.update()
# print(inv)

# pprint.pprint(inv.to_dict())
print(inventory.from_dict(inv.to_dict()))
