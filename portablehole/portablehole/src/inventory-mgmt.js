/*
Gets the weight of an inventory item.

param inventory: Object with inventory items to calculate.
return float.
 */
export const get_weight = inventory => {
    let weight = inventory.weight * inventory.quantity;

    //console.log(inventory);
    //console.log(inventory.contents);
    if (inventory.contents !== undefined){
        if (inventory.type !== 'MagicContainer'){
            weight += Object.keys(inventory.contents).reduce( (current_weight, key) => {
                current_weight += get_weight(inventory.contents[key]);
                return current_weight;
            }, 0);
        }
    }

    return weight;
};
