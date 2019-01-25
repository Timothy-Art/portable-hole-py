import {CONTAINERS, STANDALONE} from "./constants/types";

/* get_weight
Gets the weight of an inventory item.

param inventory: Object with inventory items to calculate.
return float.
 */
export const get_weight = inventory => {
    let weight = inventory.weight * inventory.quantity;

    //console.log(inventory);
    //console.log(inventory.contents);
    if (is_container(inventory)){
        if (inventory.type !== 'MagicContainer'){
            weight += Object.keys(inventory.contents).reduce( (current_weight, key) => {
                current_weight += get_weight(inventory.contents[key]);
                return current_weight;
            }, 0);
        }
    }

    return weight;
};

/* is_top_level
Determines if a key is a top level container.

param key: String with key to check.
return bool.
 */
export const is_top_level = key => (key.substr(0, 1) !== '_');

/* get_container
Gets the containing key of an item.

param key: String with key to parse.
return String with parent key.
 */
export const get_container = key => {
    let parent = key.split('_');
    console.log(parent);
    parent.pop();

    if (parent.length > 2){
        parent = parent.join('_');
    } else {
        parent = parent[1]
    }

    console.log(parent);

    return parent;
};

/* is_container
Determines if an item is a container.

param item: Item Object.
return bool.
 */
export const is_container = item => (CONTAINERS.has(item.type));

/* is_container
Determines if an item is magic.

param item: Item Object.
return bool.
 */
export const is_magic = item => (MAGIC.has(item.type));

/* is_container
Determines if an item is standalone.

param item: Item Object.
return bool.
 */
export const is_standalone = item => (STANDALONE.has(item.type));

const nest_container = ( container, inventory ) => {
    let new_container = Object.assign({}, container);
    new_container.contents = {};

    for (let key of container.contents){
        if (is_container(inventory[key])){
            new_container.contents[key] = nest_container(inventory[key], inventory);
        } else {
            new_container.contents[key] = inventory[key];
        }
        delete inventory[key];
    }

    return new_container
};

/* nest_inventory
Nests the inventory.

param inventory: Flat inventory state.
return Object.
 */
export const nest_inventory = inventory => {
    let new_inventory = Object.assign({}, inventory);

    for (let key of Object.keys(inventory)){
        if (is_top_level(key)){
            // console.log(key);
            new_inventory[key] = nest_container(new_inventory[key], new_inventory);
        }
    }

    // console.log(new_inventory);
    return new_inventory;
};

export const pretty_id = id => {
    if (is_top_level(id)){
        return id;
    }

    let pretty = id.split('_').slice(1);
    pretty = pretty.join(' > ');
    return pretty;
};

/*
Creates the id for an item being added. If container is left blank,
will return the id lowercased and cleaned.

param container: String with container id.
param name: String with name of item.
return: String with new item id.
 */
export const create_id = ( container, name ) => {
    let id = name.toLowerCase();
    let re = /(\W|_)+/g;
    id = id.replace(re, '');

    if (container !== ''){
        if (is_top_level(container)){
            id = '_' + container + '_' + id;
        } else {
            id = container + '_' + id;
        }
    }

    return id;
};

export const get_id = name => {
    return name;
};
