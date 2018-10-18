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
            contents:{
                backpack: {
                    name: 'Backpack',
                    id: 'shino.contents.backpack',
                    type: 'Container',
                    capacity: 25,
                    weight: 5,
                    value: 5,
                    quantity: 1,
                    contents: {
                        sword : {name: 'Sword', id: 'shino.contents.backpack.contents.sword0', type: 'Item', weight: 7, value: 12, quantity: 2},
                        shield : {name: 'Shield', id: 'shino.contents.backpack.contents.sword1', type: 'Item', weight: 7, value: 12, quantity: 1}
                    }
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
            contents: {
                bagofholding: {
                    name: 'Bag of Holding',
                    id: 'donny.contents.bagofholding',
                    type: 'MagicContainer',
                    capacity: 250,
                    weight: 5,
                    value: 1000,
                    quantity: 1,
                    contents: {
                        lockpick: {name: 'Lockpick', id: 'donny.contents.bagofholding.contents.lockpick', type: 'Item', weight: 1, value: 50, quantity: 1},
                        gp: {name: 'GP', id: 'donny.contents.bagofholding.contents.gp', type: 'Item', weight: 0.01, value: 1, quantity: 1000}
                    }
                }
            }
        }
    }
};

const rootReducer = (state=initialState, action) => {
    switch(action.type){
        default:
            return state;
    }
};

export default rootReducer;
