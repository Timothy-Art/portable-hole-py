import { ADD_ITEM, DELETE_ITEM } from '../constants'

export const add_item = (id, item) => ({type: ADD_ITEM, payload: {id: id, msg: item}});
export const delete_item = id => ({type: DELETE_ITEM, payload: {msg: id}});
