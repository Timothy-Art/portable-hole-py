# Portable Hole Loot Management
*The finest in loot management systems for your Dungeons and Dragons (or other tabletop) game.*

*Requires Python 3.4+*

### Getting Started

Portable Hole Loot Management Systems has been designed to run straight from the command line or IDLE Shell.

Once the script is loaded, you'll be prompted to either create a new Portable Hole, or load an existing one. There is a default save already loaded that you can play around with if you want to test some of the functionality. If you would like to start a new save, select the first option and give your new save a meaningful name. Saves are located in the `saves` folder. The save files use the `.ph` extension which is just an alias for a flat csv file.

### Using the Portable Hole

The system is operated solely by typing in commands to which the system can respond. The commands available include:

#### add [qty] [item] [,...]

Adds an item to the loot stash. [item] must be supplied, but [qty] will default to 1. An example of how this is written:
```
> add Longsword
> add 2 Chainmail
```
This can also be combined into one command using the comma separator like so.
```
> add Longsword, 2 Chainmail
```
There is no limit to how many items can be linked together by commas.

The system will also prompt you for additional information about the item, value, magic effects, and item type.

For the value of the item, previous transactions will be used to infer the value of the current item. Pressing `Enter` or `y` will accept the inferred value. Pressing `n` or supplying a numeric value will use a new value for the item.

For magic effects, you can press `Enter` or `n` if the item is non-magical or you can press `y` or provide the magic effect of the item if it is.

For miscellaneous information, you should enter in if the item is of a certain type (shown in the prompt), otherwise you can leave it blank. Misc information will be automatically inferred if there is a previous entry.

#### remove [qty] [item] [,...]

Removes an item from the stash. [item] must be supplied, but [qty] will default to 1. Just like with add, additional items can be linked together using the comma separator.
```
> remove 1 Longsword, 1 Chainmail
```
The system will cancel the transaction if you don't have enough of the item to remove from your stash.

#### sell [qty] [consigned] [item] [@ price] [,...]

Sells an item from the stash. [item] must be supplied, [qty] will default to 1, [@ price] will specify a price to sell at. Additional items can be supplied if separated with a comma. For example to sell 2 longswords at 10GP each:
```
> sell 2 Longsword @ 10
```
If you don't supply a price, the system will prompt you for how much you sold each item for. If you are selling a magical item, you can also have the system list off your magic items by selecting `y` at the prompt. If you know the exact magic effect you are looking for, you can also enter this in right from the prompt as well.

Specify `consigned` if you are selling off a consigned item.
```
> sell 3 consigned Longsword
```
This will place the consigned items back in your inventory and then sell them off.

#### buy [qty] [item] [@ price] [,...]

Buys an item. [item] must be supplied, [qty] will default to 1, [@ price] will specify a price to buy at. Additional items can be supplied if separated with a comma.
```
> buy Chainmail @ 30
```
Like with the `add` command, there will be additional prompts for you to fill in any missing information.

#### consign [qty] [item] [,...]

Puts an item on your loot sheet on consignment. [item] must be supplied, [qty] will default to 1. Additional items can be supplied if separated with a comma.
```
> consign 1 Longsword
```
This will remove the item from your inventory and place it on consignment.

#### list [magic] [consigned] [misc] [itemName] [,...]

Searches your loot sheet for specified items and lists them off to you. Additional searches can be supplied if separated with a comma and will be appended to the list. This command will list off all items named Potion off your loot sheet.
```
> list Potion
```
The list command also contains keywords that let you search for types, magic, or consigned items and can be combined with the default item names. This will list off all your magic gear:
```
> list magic
```
To list off all of your weapons and armour, you can use this:
```
> list weapons, armour
```
If you wanted to see your weapons on consignment you can type:
```
> list consigned weapons
```

#### save, s
Saves new transactions to a file. The `s` is a shortcut key if you don't want to type it all out.

#### inventory, i
Lists your entire inventory.

#### balance, b
Prints off your net worth and your liquid inventory (Coins + Gems).

#### exit, e
Exits the loot manager.
