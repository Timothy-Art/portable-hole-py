import {ADD_ITEM, DELETE_ITEM} from "../constants";

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
            contents:{
                backpack: {
                    name: 'Backpack',
                    id: 'shino.contents.backpack',
                    type: 'Container',
                    capacity: 25,
                    weight: 5,
                    value: 5,
                    quantity: 1,
                    magic: false,
                    contents: {
                        sword : {name: 'Sword', id: 'shino.contents.backpack.contents.sword', type: 'Item', weight: 7, value: 12, quantity: 2, magic: false},
                        shield : {name: 'Shield', id: 'shino.contents.backpack.contents.shield', type: 'Item', weight: 7, value: 12, quantity: 1, magic: false}
                    }
                },
                rodofsmiting: {
                    name: 'Rod of Smiting',
                    id: 'shino.contents.rodofsmiting',
                    type: 'Item',
                    weight: 5,
                    value: 2000,
                    quantity: 1,
                    magic: true
                }
            }
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
            contents: {
                bagofholding: {
                    name: 'Bag of Holding',
                    id: 'donny.contents.bagofholding',
                    type: 'MagicContainer',
                    capacity: 250,
                    weight: 5,
                    value: 1000,
                    quantity: 1,
                    magic: true,
                    contents: {
                        lockpick: {name: 'Lockpick', id: 'donny.contents.bagofholding.contents.lockpick', type: 'Item', weight: 1, value: 50, quantity: 1, magic: false},
                        gp: {name: 'GP', id: 'donny.contents.bagofholding.contents.gp', type: 'Item', weight: 0.01, value: 1, quantity: 1000, magic: false}
                    }
                }
            }
        }
    },
    counter: 0,
};

const rootReducer = (state=initialState, action) => {
    let new_state;
    switch(action.type){
        case ADD_ITEM:
            new_state = Object.assign({}, state);
            eval(`new_state.data.${action.payload.id} = action.payload.msg`);
            console.log(new_state);

            return new_state;

        case DELETE_ITEM:
            new_state = Object.assign({}, state);
            eval(`delete new_state.data.${action.payload.msg}`);
            new_state.counter += 1;
            console.log(new_state);

            return new_state;

        default:
            return state;
    }
};

export default rootReducer;
