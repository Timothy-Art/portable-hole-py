#! usr/bin/env python3
import csv
import os
import math
import logging
import re
# logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
_idcol = 10
_idcurrent = 0

#==loot_data structure========================================
# 0............item
# 1.............day
# 2........quantity
# 3..............gp
# 4...........total
# 5..........tithed
# 6............misc
# 7...........magic
# 8....magic_effect
# 9.......consigned
#=============================================================

#==query_list=================================================
# returns a list with the query results
# Parameters:
#   data........(list) of loot items
#   col.........(int) column to query
#   operator....(string) of operator (==, >, <, >=, <=)
#   value.......(variant) query value
#-------------------------------------------------------------
def query_list(data, col, operator, value):

    query = []
    logging.debug('column ' + str(col) + ' value ' + str(value))
    if operator == '==':
        for i in data:
            if i[col] == value:
                query.append(i)
    elif operator == '>':
        for i in data:
            if i[col] > value:
                query.append(i)
    elif operator == '<':
        for i in data:
            if i[col] < value:
                query.append(i)
    elif operator == '<=':
        for i in data:
            if i[col] <= value:
                query.append(i)
    elif operator == '>=':
        for i in data:
            if i[col] >= value:
                query.append(i)
    elif operator == '!=':
        for i in data:
            if i[col] != value:
                query.append(i)
    return(query)
#=============================================================

#==list_magic=================================================
# returns the magical items off the loot list, (column 7 == 1)
# Parameters:
#   data......(list) of loot items
# Returns:
#   list
#-------------------------------------------------------------
def list_magic(data):
    magic = query_list(data, 7, '==', 1)
    return(magic)
#=============================================================

#==list_money=================================================
# returns money items (cash or gems) off the loot list
# Parameters:
#   data......(list) of loot items
# Returns:
#   list
#-------------------------------------------------------------
def list_money(data):
    money = query_list(data, 6, '==', 'Coin')
    for i in query_list(data, 6, '==', 'Gem'):
        money.append(i)

    return(money)
#=============================================================

#==list_consigned=============================================
# returns consigned goods
# Parameters:
#   data......(list) of loot items
# Returns:
#   list
#-------------------------------------------------------------
def list_consigned(data):
    consigned = query_list(data, 9, '==', 1)
    print(len(consigned))
    return(consigned)
#=============================================================

#==list_spell_mats============================================
# returns spell components
# Parameters:
#   data......(list) of loot items
# Returns:
#   list
#-------------------------------------------------------------
def list_spell_mats(data):
    spell_mats = query_list(data, 6, '==', 'Spell Mats')
    return(spell_mats)
#=============================================================

#==list_untithed==============================================
# returns un-tithed earnings
# Parameters:
#   data......(list) of loot items
# Returns:
#   list
#-------------------------------------------------------------
def list_untithed(data):
    untithed = query_list(data, 5, '==', 0)
    return(untithed)
#=============================================================

#==add_item===================================================
# adds an item to the loot sheet
# Parameters:
#   data.........(list) the loot items
#   item.........(string) name of item
#   date.........(string) date received
#   quantity.....(string) number of items
#   gp...........(string) value of item
#   misc.........(string) miscellaneous information
#   magic........(string) if object is magic
#   magic_effect.(string) effects of magic
#   consigned....(int) whether to put the item on consignment
#-------------------------------------------------------------
def add_item(data, item, quantity, gp, magic, misc = 'NA', magic_effect='NA', consigned=0, date=None):
    global _idcurrent
    #Finding the total gp value of the item(s)
    if gp != 'NA':
        total = float(quantity) * float(gp)
    else:
        total = 'NA'

    if item in ['PP', 'GP', 'EP', 'SP', 'CP']:
        misc = 'Coin'
        logging.debug('New item is a coin')
    if re.search(r"(?i)gem", item):
        misc = 'Gem'
        logging.debug('New item is a gem')

    #Checking if the item needs to be tithed for
    if (misc == 'Coin' or misc == 'Gem') and int(quantity) > 0:
        tithed = 0
    elif misc == 'Coin' or misc == 'Gem':
        tithed = 1
    else:
        tithed = -1

    #Error check the magic_effect
    if magic == 0:
        magic_effect = 'NA'

    #Checking for date, otherwise set to last day
    if date is None:
        try:
            date = data[-1][1]
        except:
            date = 0

    _idcurrent += 1

    data.append([item, date, quantity, gp, total, tithed, misc, magic, magic_effect, consigned, _idcurrent-1])
    return([item, date, quantity, gp, total, tithed, misc, magic, magic_effect, consigned, _idcurrent-1])
#=============================================================

#==format_list================================================
# formats the numbers as floats instead of strings
# Parameters:
#   data...........(list) the loot items
#-------------------------------------------------------------
def format_list(data):
    global _idcol
    global _idcurrent
    _idcol = len(data[0])
    for i in range(len(data)):
        for j in (2, 3, 4, 5, 7, 9):
            try:
                data[i][j] = int(data[i][j])
            except ValueError:
                try:
                    data[i][j] = float(data[i][j])
                except ValueError:
                    data[i][j] = 'NA'
        data[i].append(_idcurrent)
        _idcurrent += 1
#=============================================================

#==get_balance================================================
# returns the net gp from the loot sheet
# Parameters:
#   data..........(list) the loot items
#-------------------------------------------------------------
def get_balance(data):
    balance = 0
    for i in data:
        try:
            balance = balance + i[4]
        except:
            pass
    return(balance)
#=============================================================

#==get_cash===================================================
# returns the net gp of liquid items
# Parameters:
#   data............(list) the loot items
#-------------------------------------------------------------
def get_money(data):
    return(round(get_balance(list_money(data)), 2))
#=============================================================

#==build_inventory============================================
# builds an inventory dictionary based on the loot sheet
# Parameters:
#   data............(list) the loot items
# Returns:
#   dictionary
#-------------------------------------------------------------
def build_inventory(data):
    inventory = {}
    for i in data:
        if i[7] == 1:
            inventory.setdefault(i[0]+' '+i[8], [0, 0])
            inventory[i[0]+' '+i[8]] = [inventory[i[0]+' '+i[8]][0] + i[2], i[3]]
            if inventory[i[0]+' '+i[8]][0] == 0:
                del inventory[i[0]+' '+i[8]]
        else:
            inventory.setdefault(i[0], [0, 0])
            inventory[i[0]] = [inventory[i[0]][0] + i[2], i[3]]
            if inventory[i[0]][0] == 0:
                del inventory[i[0]]
    return(inventory)
#=============================================================

#==tithe======================================================
# tithes automatically
# Parameters:
#   data.............(list) the loot items
#-------------------------------------------------------------
def tithe(data):
    untithed = get_balance(list_untithed(data))
    add_item(data, 'GP', untithed * 0.025, 1, 0, Tithe, 'NA')
    for i in range(len(data)):
        if (data[i][6]== 'Coin' or data[i][6] == 'Gem') and data[i][5] == 0:
            data[i][5] = 1
    return(untithed*0.025)
#=============================================================

#==sell=======================================================
# Records a sell transaction in the loot sheet
# Parameters:
#   data.............(list) of loot items
#   item.............(string) the item to sell
#   quantity.........(int) the number of items
#   price............(int) the sale price of the item
#-------------------------------------------------------------
def sell(data, item, quantity, price, magic_effect='NA', misc='NA'):
    item_list = query_list(data, 0, '==', item)
    item_list = query_list(item_list, 8, '==', magic_effect)
    item_dict = build_inventory(item_list)

    if magic_effect != 'NA':
        itemName = item + " " + magic_effect
    else:
        itemName = item

    logging.debug(item_dict)

    logging.debug('Check count: ' + str(item_dict[itemName][0]))

    if item_dict[itemName][0] >= quantity:
        add_item(data, item, -quantity, item_list[0][3], magic_effect != 'NA', misc,
                  magic_effect)
        add_item(data, 'GP', price*quantity, 1, 0, 'Coin', 'NA')
        return(item_list[0][3]*quantity)
    else:
        raise Exception('Insufficient Quantity')
#=============================================================

#==purchase===================================================
# Records a purchase transaction
# Parameters:
#   data.............(list) of loot items
#   item.............(string) item to purchase
#   gems.............(boolean) whether to use gems?
#   stock............(boolean) if the item is going to stock?
#   paid.............(float) paid amount
#   quantity.........(int) number of items
#   gp...............(float) gp price of item
#   magic............(int) if item is magical
#   misc.............(string) misc information
#   effect...........(string) magic effect
#   date.............(string) date purchased
#-------------------------------------------------------------
def purchase(data, item, gems, stock, paid, quantity, gp, magic, misc='NA', effect='NA', date=None):
    length = len(data)
    money_out = []
    if gems == 1:
        money = list_money(data)
    else:
        money = query_list(data, 6, '==', 'Coin')

    money = build_inventory(money)

    logging.debug(money)

    total = 0
    for i in money.keys():
        total = total + money[i][0]*money[i][1]

    if (gp * quantity) <= total:
        if stock:
            add_item(data, item, quantity, gp, magic, misc, effect, date)
            logging.debug("Added transaction")

        for i in money.keys():
            logging.debug(i)
            if money[i][1] <= paid:
                amount = (paid - (paid % money[i][1]))/money[i][1]
                amount = math.ceil(amount)
                logging.debug(str(paid) + '%' + str(money[i][1]) + '=' + str(amount))
                if amount > money[i][0]:
                    amount = money[i][0]
                    logging.debug('capped!')
                money_out.append(add_item(data, i, -amount, money[i][1], 0, misc = 'Purchased ' + item, date = date))
                paid = paid - (amount*money[i][1])
                logging.debug(i + ' | ' + str(money[i][1]) + ' | ' + str(amount) + ' = ' + str(paid))

        if paid > 0:
            for i in range(length, len(data)-1):
                data.pop()
            print(paid)
            return("Need smaller denominations")
    else:
        return("Insufficient Funds")

    return(money_out)
#=============================================================

#==convert_gp=================================================
# Converts smaller money items(EP, SP, CP) to GP
# Parameters:
#   data...........(list) of loot items
#=============================================================
def convert_gp(data):
    money = []
    items = ["EP", "SP", "CP"]
    for i in items:
        for j in query_list(data, 0, '==', i):
            money.append(i)
    money_dict = build_inventory(money)
    for i in money_dict:
        con = (i[0]-(i[0]%(1/i[1])))/(1/i[1])
        if con > 0:
            add_item(data, i.keys(), -con*(1/i[1]), i[0], 0, 'Coin')
            add_item(data, 'GP', con, 1, 0, 'Coin')
    return(con)
#=============================================================

#==add========================================================
# Provides prompts to add items to the loot list
# Parameters:
#   data...........(list) of loot items
#   params.........(list) of items to add
#=============================================================
def add(data, params):
    out = ""
    append = ""

    for item in params:
        qty, name, val, magic_effect, magic, misc = None, None, None, None, None, None

        try:
            qty = int(item[0])
            name = " ".join(str(x) for x in item[1:]).strip()
        except ValueError:
            qty = 1
            name = " ".join(str(x) for x in item[0:]).strip()

        # print(name, qty)
        #-- Searching for previous entries and assuming the value of item -----
        found = query_list(data, 0, '==', name)

        if found:
            val = found[0][3]
            found_misc = found[0][6]
            newval = None

            if found_misc not in ["Coin"]:
                print("Value of", name, "should be", val, "GP, is this correct?")
                newval = input()

            if newval and newval not in ['y', 'Y', 'yes', 'Yes']:
                val = False
                while not val:
                    try:
                        val = float(newval)
                    except ValueError:
                        print("Please enter the correct value:")
                        newval = input()
        else:
            val = False
            found_misc = "NA"
            print("Value of", name + "?")
            newval = input()
            while not val:
                try:
                    val = int(newval)
                except ValueError:
                    print("Please enter a numeric value:")
                    newval = input()
        #----------------------------------------------------------------------

        #-- Getting remaining information -------------------------------------
        if found_misc not in ["Coin", "Gem", "Spell Mat"]:
            print("Any magic effects?")
            magic_effect = input()
        else:
            magic_effect = ''

        if magic_effect in ["yes", "Yes", "y", "Y"]:
            print("Effect?")
            magic_effect = input()
        elif magic_effect in ["no", "No", "n", "N"]:
            magic_effect = ''

        magic = 1 if magic_effect else 0

        if found_misc not in ["Coin", "Gem", "Spell Mat", "Weapon", "Armour", "Ammunition", "Art"]:
            print("Item type? (Coin, Gem, Spell Mat, Weapon, Armour, Ammunition, Art):")
            misc = input()

        misc = misc if misc else found_misc

        add_item(data, name, qty, val, magic, misc, magic_effect)
        out = out + append + str(qty) + " " + name + magic_effect + " added to the stash."
        append = ", "
    out = out
    return(out)

#==remove=====================================================
# Provides prompts to remove items from the loot list
# Parameters:
#   data...........(list) of loot items
#   params.........(list) of items to remove
#=============================================================
def remove(data, params):
    out = ""
    append = ""
    item_dict = build_inventory(data)

    for item in params:
        qty, name, val, magic_effect, magic, misc = None, None, None, None, None, None

        try:
            qty = -int(item[0])
            name = " ".join(str(x) for x in item[1:]).strip()
        except ValueError:
            qty = -1
            name = " ".join(str(x) for x in item[0:]).strip()

        # print(name, qty)

        #-- Getting remaining information -------------------------------------
        #-- Searching for previous entries and assuming the value of item -----
        found = query_list(data, 0, '==', name)

        if found:
            if found[0][6] not in ["Coin", "Gem", "Spell Mat"]:
                print("Looking for a magical " + name + "?")
                magic_effect = input()
            else:
                magic_effect = ''

            if magic_effect in ["yes", "Yes", "y", "Y"]:
                magic_list = query_list(found, 7, '==', 1)
                magic_set = {}

                for n in magic_list:
                    if (n[0], n[8]) in magic_set.keys():
                        magic_set[(n[0], n[8])] += n[2]
                        if magic_set[(n[0], n[8])] <= 0:
                            del magic_set[(n[0], n[8])]
                    else:
                        magic_set[(n[0], n[8])] = n[2]

                logging.debug(magic_set)

                if len(magic_set) == 0:
                    print("You don't have any magic", name)
                    magic_effect = ''
                else:
                    print("Use the numbers to make your selection")

                    l = [(i, k[0], k[1]) for i, k in enumerate(magic_set.keys())]
                    [print(str(i[0]) + ": " + i[1] + " " + i[2]) for i in l]
                    magic_effect = input()
                    #print(l)

                    try:
                        magic_effect = l[int(magic_effect)][2]
                    except:
                        print("That's not in the stash.")
                        return(out)
            elif magic_effect in ["no", "No", "n", "N"]:
                magic_effect = ''

            magic = 1 if magic_effect else 0
            magic_effect = " "+magic_effect if magic_effect else ""


            if found and name+magic_effect in item_dict.keys() and -qty <= item_dict[name+magic_effect][0]:
                val = found[0][3]
                add_item(data, name, qty, val, magic, found[0][6], magic_effect.strip())
                out = out + append + str(-qty) + " " + name + magic_effect + " removed from the stash."
            else:
                out += append + "you don't have enough", name
            #----------------------------------------------------------------------
            append = ", "
        else:
            out += append + "you don't have any " + name
            append = ", "
    return(out)

#==sellItem===================================================
# Provides prompts to sell items off the loot list
# Parameters:
#   data...........(list) of loot items
#   params.........(list) of items to remove
#=============================================================
def sellItem(data, params):
    out = ""
    append = ""

    for item in params:
        qty, name, price, magic_effect = None, None, None, None

        try:
            at = item.index('@')
        except ValueError:
            at = -1

        if at != -1:
            price = item[at+1]
            item = item[0:at]

        try:
            consign = item.index('consigned')
        except ValueError:
            consign = -1

        if consign != -1:
            item.remove("consigned")

        try:
            qty = int(item[0])
            name = " ".join(str(x) for x in item[1:]).strip()
        except ValueError:
            qty = 1
            name = " ".join(str(x) for x in item[0:]).strip()

        found = query_list(data, 0, '==', name)

        if consign != -1:
            found = query_list(found, 9, '==', 1)

        if found:
            if found[0][6] not in ["Coin", "Gem", "Spell Mat"]:
                print("Looking for a magical " + name + "?")
                magic_effect = input()
            else:
                magic_effect = ''

            if magic_effect in ["yes", "Yes", "y", "Y"]:
                magic_list = query_list(found, 7, '==', 1)
                magic_set = {}

                for n in magic_list:
                    if (n[0], n[8]) in magic_set.keys():
                        magic_set[(n[0], n[8])] += n[2]
                        if magic_set[(n[0], n[8])] <= 0:
                            del magic_set[(n[0], n[8])]
                    else:
                        magic_set[(n[0], n[8])] = n[2]

                logging.debug(magic_set)

                if len(magic_set) == 0:
                    print("You don't have any magic", name)
                    magic_effect = ''
                else:
                    print("Use the numbers to make your selection")

                    l = [(i, k[0], k[1]) for i, k in enumerate(magic_set.keys())]
                    [print(str(i[0]) + ": " + i[1] + " " + i[2]) for i in l]
                    magic_effect = input()
                    #print(l)
                    try:
                        magic_effect = " " + l[int(magic_effect)][2]
                    except:
                        out += append + "you don't have " + str(qty) + " " + name
                        continue
            elif magic_effect in ["no", "No", "n", "N"]:
                magic_effect = ""

            misc = found[0][6]

            while not price:
                try:
                    if consign == -1:
                        print("How much are you selling the " + name + magic_effect + " for?")
                        price = float(input())
                    else:
                        print("How much are you receiving for the " + name + magic_effect + "?")
                        price = float(input())
                except:
                    print("Please enter a number in GP.")

            try:
                if consign == -1:
                    sell(data, name, qty, int(price), "NA" if magic_effect == "" else magic_effect.strip(), misc)
                    out += append + str(qty) + " " + name + magic_effect + " sold for " + str(qty*int(price)) + "GP"
                else:
                    add_item(data, name, qty, found[0][3], magic_effect != '', misc, 'NA' if magic_effect == '' else magic_effect.strip(), consigned = 1)
                    sell(data, name, qty, int(price), "NA" if magic_effect == "" else magic_effect.strip(), misc)
                    out += append  + "received " + str(qty*int(price)) + "GP for " + str(qty) + " " + name + magic_effect

                append = ", "
            except:
                out += append + "you don't have " + str(qty) + " " + name
                append = ", "
        else:
            out += append + "you don't have any " + name
    return(out)

#==buyItem====================================================
# Provides prompts to buy an item
# Parameters:
#   data...........(list) of loot items
#   params.........(list) of items to buy
#=============================================================
def buyItem(data, params):
    out = ""
    append = ""

    for item in params:
        qty, name, price, magic, magic_effect, misc = None, None, None, None, None, None

        try:
            at = item.index('@')
        except ValueError:
            at = -1

        if at != -1:
            price = item[at+1]
            item = item[0:at]

        try:
            qty = int(item[0])
            name = " ".join(str(x) for x in item[1:]).strip()
        except ValueError:
            qty = 1
            name = " ".join(str(x) for x in item[0:]).strip()

        found = query_list(data, 0, '==', name)

        if found:
            val = found[0][3]
            found_misc = found[0][6]
            print("Value of", name, "should be", val, "GP, is this correct?")
            newval = input()

            if newval and newval not in ['y', 'Y', 'yes', 'Yes']:
                val = False
                while not val:
                    try:
                        val = int(newval)
                    except ValueError:
                        print("Please enter the correct value:")
                        newval = input()
        else:
            val = False
            found_misc = "NA"
            print("Value of", name + "?")
            newval = input()
            while not val:
                try:
                    val = int(newval)
                except ValueError:
                    print("Please enter a numeric value:")
                    newval = input()
        #----------------------------------------------------------------------

        #-- Getting remaining information -------------------------------------
        if found_misc not in ["Coin", "Gem", "Spell Mat"]:
            print("Any magic effects?")
            magic_effect = input()
        else:
            magic_effect = ''

        if magic_effect in ["yes", "Yes", "y", "Y"]:
            print("Effect?")
            magic_effect = input()
        elif magic_effect in ["no", "No", "n", "N"]:
            magic_effect = ''

        magic = 1 if magic_effect else 0

        if found_misc not in ["Coin", "Gem", "Spell Mat", "Weapon", "Armour", "Ammunition", "Art"]:
            print("Item type? (Coin, Gem, Spell Mat, Weapon, Armour, Ammunition, Art):")
            misc = input()

        misc = misc if misc else found_misc
        #----------------------------------------------------------------------

        try:
            logging.debug("Price set at " + price)
            price = float(price)
        except:
            logging.debug("Reset Price")
            price = None

        while not price:
            try:
                print("How much are you buying each " + name + magic_effect + " for?")
                price = float(input())
            except:
                print("Please enter a number in GP.")

        print("Put in the stash?")
        stock = input()
        if re.search(stock, r"^[nN]"):
            stock = False
        else:
            stock = True

        money_out = purchase(data, name, True, stock, price*qty, qty, val, magic, misc, magic_effect)
        if type(money_out) == list:
            out += append + str(qty) + " " + name + magic_effect + " purchsed for " + " ".join([str(-i[2]) + " " + i[0] + " " for i in money_out])
            append = ", "
        else:
            out += append + money_out + " for " + str(qty) + " " + name + magic_effect

    return(out)

#==listItem===================================================
# Provides prompts to list inventory items
# Parameters:
#   data...........(list) of loot items
#   params.........(list) of items to buy
#=============================================================
def listItem(data, params):
    # print(params)
    out = []

    for param in params:
        loot = data
        param = set(param)

        logging.debug(param)
        if 'Magic' in param or 'magic' in param:
            loot = list_magic(data)
            param.difference_update(['Magic', 'magic'])

        if 'Consigned' in param or 'consigned' in param:
            loot = list_consigned(loot)
            param.difference_update(['Consigned', 'consigned'])

        if 'Money' in param or 'money' in param:
            loot = list_money(loot)
            param.difference_update(['Money', 'money'])

        if any(x in ['Coin', 'coin', 'Coins', 'coins'] for x in param):
            loot = query_list(loot, 6, '==', 'Coin')
            param.difference_update(['Coin', 'coin', 'Coins', 'coins'])

        if any(x in ['Gem', 'gem', 'Gems', 'gems'] for x in param):
            loot = query_list(loot, 6, '==', 'Gem')
            param.difference_update(['Gem', 'gem', 'Gems', 'gems'])

        if any(x in ['Weapon', 'weapon', 'Weapons', 'weapons'] for x in param):
            loot = query_list(loot, 6, '==', 'Weapon')
            param.difference_update(['Weapon', 'weapon', 'Weapons', 'weapons'])

        if any(x in ['Armour', 'armour', 'Armor', 'armor'] for x in param):
            loot = query_list(loot, 6, '==', 'Armour')
            param.difference_update(['Armour', 'armour', 'Armor', 'armor'])

        if any(x in ['Ammunition', 'ammunition'] for x in param):
            loot = query_list(loot, 6, '==', 'Ammunition')
            param.difference_update(['Ammunition', 'ammunition'])

        if any(x in ['Materials', 'materials', 'Spell', 'spell', 'Mats', 'mats'] for x in param):
            loot = query_list(loot, 6, '==', 'Spell Mat')
            param.difference_update(['Materials', 'materials', 'Spell', 'spell', 'Mats', 'mats'])

        if len(param) > 0:
            for item in param:
                loot = query_list(loot, 0, '==', item)

        [out.append(line) for line in loot]

    logging.debug(out)
    checks = set()
    for i, line in reversed(list(enumerate(out))):
        if line[_idcol] in checks:
            del out[i]
        else:
            checks.add(line[_idcol])

    logging.debug(out)

    return(buildLootTable(build_inventory(out)))

#==consignItem================================================
# Provides prompts to consign items on the loot list
# Parameters:
#   data...........(list) of loot items
#   params.........(list) of items to remove
#=============================================================
def consignItem(data, params):
    out = ""
    append = ""

    for item in params:
        qty, name, price, magic_effect = None, None, None, None

        try:
            at = item.index('@')
        except ValueError:
            at = -1

        if at != -1:
            price = item[at+1]
            item = item[0:at]

        try:
            qty = int(item[0])
            name = " ".join(str(x) for x in item[1:]).strip()
        except ValueError:
            qty = 1
            name = " ".join(str(x) for x in item[0:]).strip()

        found = query_list(data, 0, '==', name)

        if found:
            if found[0][6] not in ["Coin", "Gem", "Spell Mat"]:
                print("Looking for a magical " + name + "?")
                magic_effect = input()
            else:
                magic_effect = ''

            if magic_effect in ["yes", "Yes", "y", "Y"]:
                magic_list = query_list(found, 7, '==', 1)
                magic_set = {}

                for n in magic_list:
                    if (n[0], n[8]) in magic_set.keys():
                        magic_set[(n[0], n[8])] += n[2]
                        if magic_set[(n[0], n[8])] <= 0:
                            del magic_set[(n[0], n[8])]
                    else:
                        magic_set[(n[0], n[8])] = n[2]

                logging.debug(magic_set)

                if len(magic_set) == 0:
                    print("You don't have any magic", name)
                    magic_effect = ''
                else:
                    print("Use the numbers to make your selection")

                    l = [(i, k[0], k[1]) for i, k in enumerate(magic_set.keys())]
                    [print(str(i[0]) + ": " + i[1] + " " + i[2]) for i in l]
                    magic_effect = input()
                    #print(l)

                    try:
                        magic_effect = " " + l[int(magic_effect)][2]
                    except:
                        print("That's not in the stash.")
                        return(out)
            elif magic_effect in ["no", "No", "n", "N"]:
                magic_effect = ""

            misc = found[0][6]

            item_dict = build_inventory(found)

            logging.debug(item_dict)

            logging.debug('Check count: ' + str(item_dict[name+magic_effect][0]))

            if item_dict[name+magic_effect][0] >= -qty:
                add_item(data, name, qty, found[0][3], magic_effect != '', misc, 'NA' if magic_effect == '' else magic_effect.strip(), consigned = 1)
                out += append + str(qty) + " " + name + magic_effect + " consigned"
                append = ", "
            else:
                out += append + "you don't have " + str(qty) + " " + name + " to consign"
                append = ", "
        else:
            out += append + "you don't have any " + name
            append = ", "
    return(out)

#==buildLootTable=============================================
# Builds a formatted string for loot tables.
# Parameters:
#   inventory.......(dict) of inventory
#=============================================================
def buildLootTable(inventory):
    if len(inventory) == 0:
        return("Item | Qty | Value \n-----|-----|-------")

    itemLen = max(min(len(max(inventory.keys(), key=len)), 50), 4)
    qtyLen = max(len(str(inventory[max(inventory, key=lambda x : len(str(inventory[x][0])))][0])), 3)
    valLen = max(len(str(inventory[max(inventory, key=lambda x : len(str(inventory[x][1])))][1])),5)

    out = "Item"+" "*(itemLen-4)+" | Qty"+" "*(qtyLen-3)+" | Value"+" "*(valLen-5)+"\n"+"-"*itemLen+"-|-"+"-"*qtyLen+"-|-"+"-"*valLen+"\n"

    for item in inventory.keys():
        qty = str(inventory[item][0])
        val = str(inventory[item][1])

        out = out + item+" "*(itemLen-len(item))+" | "+" "*(qtyLen-len(qty))+qty+" | "+" "*(valLen-len(val))+val+"\n"
    return(out)

print("====================================================\\\n"+
      "Welcome to PORTABLE HOLE(tm) Loot Management Systems \\\n"+
      "======================================================\\\n")

print("(1) New Portable Hole\n(2) Use Existing Portable Hole")
selection = 0

while selection != '1' and selection != '2':
    selection = input()

if selection == '2':
    saves = os.listdir("./saves")
    saves = [save for save in saves if save.endswith('.ph')]

    if len(saves) == 0:
        print("No portable holes found, creating a new one...")
        selection = '1'

    selection = -1

    print("Use the numbers to make your selection:")
    for i, save in enumerate(saves):
        print("("+str(i+1)+") "+save[:len(save)-3])

    while selection < 0 or selection > len(saves)-1:
        try:
            selection = int(input())-1
        except:
            selection = -1

    name = saves[selection]
    loot_file = open('saves/'+name)
    loot_reader = csv.reader(loot_file)
    loot_data = list(loot_reader)

    if loot_data:
        format_list(loot_data)

    selection = '2'

if selection == '1':
    print("Name:")
    name = input()
    name += ".ph"
    loot_file = open('saves/'+name, 'w+')
    loot_data = []

logging.debug("_idcol = " + str(_idcol))
message = ""

while True:
    print("How may I serve you?")
    command = input()
    command = command.split(' ', 1)
    fn = command[0]

    if fn in ["help", "Help", "h", "H"]:
        print("Available Commands:\n\n"+
        "(1)  add [qty] [item] [,...] - Adds an item to the loot stash. [item] must be supplied, but [qty] will default to 1. Additional items can be supplied if separated with a comma.\n\n"+
        "(2)  remove [qty] [item] [,...] - Removes an item from the stash. [item] must be supplied, but [qty] will default to 1. Additional items can be supplied if separated with a comma.\n\n"+
        "(3)  sell [qty] [consigned] [item] [@ price] [,...] - Sells an item from the stash. [item] must be supplied, [qty] will default to 1, [@ price] will specify a price to sell at. Specify 'consigned' if you are selling off a consigned item. Additional items can be supplied if separated with a comma.\n\n"+
        "(4)  buy [qty] [item] [@price] [,...] - Buys an item. [item] must be supplied, [qty] will default to 1, [@ price] will specify a price to buy at. Additional items can be supplied if separated with a comma.\n\n"+
        "(5)  list [misc] [magic] [itemName] [,...] - Searches your loot sheet for specified items and lists them off to you. Additional searches can be supplied if separated with a comma and will be appended to the list.\n\n"+
        "(6)  consign [qty] [item] [,...] - Puts an item on your loot sheet on consignment. [item] must be supplied, [qty] will default to 1. Additional items can be supplied if separated with a comma.\n\n"+
        "(7)  save - Saves new transactions to a file.\n\n"+
        "(8)  inventory - Lists your entire inventory.\n\n"+
        "(9)  balance - Prints off your net worth and your liquid inventory (Coins + Gems).\n\n"+
        "(10) exit - Exits the loot manager.\n"
        )
        continue
    elif fn in ["exit", "Exit", "e", "E"]:
        print("Bye :)")
        break
    elif fn in ["hello", "Hello", "hi", "Hi"]:
        print("Greetings!")
        continue
    elif fn in ["save", "Save", "s", "S"]:
        print("Saving Transactions...")
        with open("saves/"+name, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            for line in loot_data:
                writer.writerow(line[0:_idcol])
        continue
    elif fn in ["Inventory", "inventory", "I", "i"]:
        print(buildLootTable(build_inventory(loot_data)))
        continue
    elif fn in ["Balance", "balance", "B", "b"]:
        print("Net Worth: " + str(get_balance(loot_data)) + "GP\nLiquid:    " + str(get_money(loot_data)) + "GP")
        continue

    try:
        # pprint.pprint(command)
        params = command[1].split(',')
        params = [s.strip().split() for s in params]

        #print("Function", fn)
        #print("Params", params)

    except:
        print("I'm not sure what you meant...")
        continue

    if fn in ['add', 'Add']:
        message = add(loot_data, params)
    elif fn in ['remove', 'Remove']:
        message = remove(loot_data, params)
    elif fn in ['sell', 'Sell']:
        message = sellItem(loot_data, params)
    elif fn in ['buy', 'Buy']:
        message = buyItem(loot_data, params)
    elif fn in ['list', 'List']:
        message = listItem(loot_data, params)
    elif fn in ['consign', 'Consign']:
        message = consignItem(loot_data, params)

    if message != '' : print(message)
    message = ''
