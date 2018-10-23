import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import {get_weight, nest_inventory} from "../inventory-mgmt";
import { delete_item } from '../actions';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import * as fas from '@fortawesome/pro-solid-svg-icons';
import Grid from "./grid";
import './css/inventory.css';

const map_state_to_inventory = state => ({
    data: state.data,
    counter: state.counter
});


const map_dispatch_to_inventory = dispatch => ({
    delete_item: id => dispatch(delete_item(id))
});

const ItemButton = ({ icon, fn }) => (
    <a className={'item-btn'} onClick={fn}>
        <FontAwesomeIcon icon={icon} fixedWidth={false}/>
    </a>
);

const ItemControls = ({ move_fn, sell_fn, dele_fn }) => (
    <div className={'item-controls column is-narrow has-text-right'}>
        <ItemButton icon={fas.faArrowsAlt} fn={move_fn} />
        <ItemButton icon={fas.faDollarSign} fn={sell_fn} />
        <ItemButton icon={fas.faTimes} fn={dele_fn} />
    </div>
);

class Item extends Component {
    static propTypes = {
        id: PropTypes.string.isRequired,
        name: PropTypes.string.isRequired,
        quantity: PropTypes.number.isRequired,
        magic: PropTypes.bool.isRequired,
        move_fn: PropTypes.func,
        sell_fn: PropTypes.func,
        dele_fn: PropTypes.func
    };

    render(){
        let magic = this.props.magic ? 'magic' : '';
        console.log(`${this.props.id} Rendering`);

        return(
            <div className={'columns is-mobile no-gap item ' + magic}>
                <div className={'item-stat column is-narrow'}>
                    {this.props.name}
                </div>
                <div className={'item-stat column has-text-left'}>
                    {this.props.quantity > 1 ? 'x' + this.props.quantity.toFixed(0) : ''}
                </div>
                <ItemControls
                    move_fn={ () => this.props.move_fn(this.props.id) }
                    sell_fn={ () => this.props.sell_fn(this.props.id) }
                    dele_fn={ () => this.props.dele_fn(this.props.id) }
                />
            </div>
        )
    }
}

class Container extends Component {
    static propTypes = {
        container: PropTypes.shape({
            id: PropTypes.string,
            name: PropTypes.string,
            type: PropTypes.string,
            capacity: PropTypes.number,
            quantity: PropTypes.number,
            value: PropTypes.number,
            weight: PropTypes.number,
            magic: PropTypes.bool,
            contents: PropTypes.object
        }),
        dele_fn: PropTypes.func
    };

    constructor(props){
        super(props);
        console.log(this.props);
        this.state = {
            collapsed: false
        };

        this.collapse = this.collapse.bind(this);
    }

    get_contents(){
        return(Object.keys(this.props.container.contents).reduce( (current_weight, key) => {
            current_weight += get_weight(this.props.container.contents[key]);
            return current_weight;
        }, 0))
    }

    get_weight(){
        return get_weight(this.props.container);
    }

    collapse(){
        this.setState({collapsed: !this.state.collapsed});
    }

    render(){
        let container = this.props.container;
        let magic = container.magic ? 'magic' : '';
        console.log(`${container.id} Rendering`);

        return(
            <div className={this.state.collapsed ? 'con collapsed ' + magic : 'con ' + magic}>
                <div className={'con-item columns is-mobile no-gap is-marginless is-paddingless'}>
                    <div className={'item-stat column is-narrow'}>
                        {container.name}
                    </div>
                    <div className={'item-controls column is-narrow'}>
                        <ItemButton icon={this.state.collapsed ? fas.faAngleUp : fas.faAngleDown} fn={this.collapse} />
                    </div>
                    <div className={'item-stat warning column has-text-right'}>
                        {this.get_contents()} | {container.capacity}
                    </div>
                    <ItemControls dele_fn={() => this.props.dele_fn(container.id)}/>
                </div>
                <div className={'container-contents'}>
                    {
                        Object.keys(container.contents).map( key => {
                            let item = container.contents[key];
                            if (item.type === 'Container' || item.type === 'MagicContainer'){
                                return(<Container container={item} dele_fn={this.props.dele_fn} key={key} />)
                            } else {
                                return(
                                    <Item
                                        id={item.id}
                                        name={item.name}
                                        quantity={item.quantity}
                                        magic={item.magic}
                                        dele_fn={this.props.dele_fn}
                                        key={key}
                                    />
                                )
                            }
                        } )
                    }
                </div>
            </div>
        )
    }
}

class ConnectedInventory extends Component {
    constructor(props){
        super(props);

        console.log(this.props.data);
        console.log(this.props);
    }

    render(){
        let data = nest_inventory(this.props.data);

        return(
            <Grid>
                {
                    Object.keys(data).map( key => (
                        <Container container={data[key]} dele_fn={this.props.delete_item} key={key} />
                    ))
                }
            </Grid>
        )
    }
}

const Inventory = connect(map_state_to_inventory, map_dispatch_to_inventory)(ConnectedInventory);

export default Inventory;
