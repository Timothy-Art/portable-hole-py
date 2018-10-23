import { ADD_ITEM, DELETE_ITEM } from "../constants";
import {is_container, get_container, is_top_level} from "../inventory-mgmt";

const initialState = {
    user: {name: 'timbit'},
    data: {
        shino: {
            name: 'Shino',
            id: 'shino',
            type: 'Player',
            capacity: 255,
            weight: 0,
            value: 0,
            quantity: 1,
            magic: false,
            contents: ['_shino_backpack', '_shino_rodofsmiting']
        },
        _shino_backpack: {
            name: 'Backpack',
            id: '_shino_backpack',
            type: 'Container',
            capacity: 25,
            weight: 5,
            value: 5,
            quantity: 1,
            magic: false,
            contents: ['_shino_backpack_sword', '_shino_backpack_shield']
        },
        _shino_backpack_sword: {
            name: 'Sword', id: '_shino_backpack_sword', type: 'Item', weight: 7, value: 12, quantity: 2, magic: false
        },
        _shino_backpack_shield: {
            name: 'Shield', id: '_shino_backpack_shield', type: 'Item', weight: 7, value: 12, quantity: 1, magic: false
        },
        _shino_rodofsmiting: {
            name: 'Rod of Smiting',
            id: '_shino_rodofsmiting',
            type: 'Item',
            weight: 5,
            value: 2000,
            quantity: 1,
            magic: true
        },
        donny: {
            name: 'Donny',
            id: 'donny',
            type: 'Player',
            capacity: 110,
            weight: 0,
            value: 0,
            quantity: 1,
            magic: false,
            contents: ['_donny_bagofholding']
        },
        _donny_bagofholding: {
            name: 'Bag of Holding',
            id: '_donny_bagofholding',
            type: 'MagicContainer',
            capacity: 250,
            weight: 5,
            value: 1000,
            quantity: 1,
            magic: true,
            contents: ['_donny_bagofholding_lockpick', '_donny_bagofholding_gp']
        },
        _donny_bagofholding_lockpick: {name: 'Lockpick', id: '_donny_bagofholding_lockpick', type: 'Item', weight: 1, value: 50, quantity: 1, magic: false},
        _donny_bagofholding_gp: {name: 'GP', id: '_donny_bagofholding_gp', type: 'Item', weight: 0.01, value: 1, quantity: 1000, magic: false}
    },
    items: [
        {name: 'Sword', type: 'Item', weight: 7, value: 12, magic: false},
        {name: 'Shield', type: 'Item', weight: 7, value: 12, magic: false}
    ]
};

/*
Deletes an item and cascades down contents if available.
 */
const delete_cascade = (state, id) => {
    let item = id;

    if (!is_top_level(item)){
        let parent = get_container(item);
        state[parent].contents.splice(state[parent].contents.indexOf(item), 1);
    }

    if (is_container(state[item])){
        for (let i = state[item].contents.length-1; i >= 0; i--){
            delete_cascade(state, state[item].contents[i]);
        }
    }

    delete state[item];

    return state
};

const rootReducer = (state=initialState, action) => {
    switch(action.type){
        case ADD_ITEM:
            let add_state = Object.assign({}, state);

            return add_state;

        case DELETE_ITEM:
            let del_state = Object.assign({}, state.data);

            delete_cascade(del_state, action.payload.msg);
            // send delete through socket -> else cache?

            return Object.assign({}, {data: del_state});

        default:
            return state;
    }
};

export default rootReducer;
