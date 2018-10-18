const initialState = {
    user: {name: 'timbit'},
    data: {
        Shino: {
            name: 'Shino',
            id: 'Shino',
            type: 'Player',
            capacity: 255,
            weight: 0,
            value: 0,
            contents:{
                backpack: {
                    name: 'backpack',
                    id: 'Shino.contents.backpack',
                    type: 'Container',
                    capacity: 25,
                    weight: 5,
                    value: 5,
                    contents: {
                        sword0 : {name: 'sword', id: 'Shino.contents.backpack.contents.sword0', type: 'Item', weight: 7, value: 12},
                        sword1 : {name: 'sword', id: 'Shino.contents.backpack.contents.sword1', type: 'Item', weight: 7, value: 12}
                    }
                }
            }
        }
    }
};

const rootReducer = (state=initialState, action) => {
    console.log(state);
    switch(action.type){
        default:
            return state;
    }
};

export default rootReducer;
