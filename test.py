import item
import collection
import container

arrows = collection.Collection(item=item.Item(name="Arrow", weight=0.1, value=0.1, category='ammunition'), quantity=10)
sword = collection.Collection(item=item.MagicItem(name="Sword", magic="+1", weight=2, value=10, category='weapon'))

# print(arrows)
# print(sword)

arrows += 10

quiver = container.Container(name="Quiver", capacity=4, weight=2, value=1)
backpack = container.Container(name='Backpack', capacity=20, weight=5, value=2)
backpack.add(quiver, sword, sword, arrows)
quiver.add(arrows, arrows)

print(backpack)

search = backpack.search(magic=True)
for i in search:
    print(i)

print(backpack)

