import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { get_weight } from "../inventory-mgmt";
import store from "../store";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import * as fas from '@fortawesome/pro-solid-svg-icons';
import Grid from "./grid";
import './css/inventory.css';

const map_state_to_inventory = state => ({
   data: state.data
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
    render(){
        return(
            <div className={'item columns is-mobile no-gap is-marginless is-paddingless'}>
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

Item.propTypes = {
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    quantity: PropTypes.number.isRequired,
    move_fn: PropTypes.func,
    sell_fn: PropTypes.func,
    dele_fn: PropTypes.func
};

class Container extends Component {
    constructor(props){
        super(props);

        this.state = {
            contents_weight: this.get_contents(),
            current_weight: this.get_weight(),
            collapsed: false
        };

        this.collapse = this.collapse.bind(this);
    }

    get_contents(){
        return Object.keys(this.props.container.contents).reduce( (current_weight, key) => {
            current_weight += get_weight(this.props.container.contents[key]);
            return current_weight;
        }, 0);
    }

    get_weight(){
        return get_weight(this.props.container);
    }

    collapse(){
        this.setState({collapsed: !this.state.collapsed});
    }

    render(){
        let container = this.props.container;
        console.log(`${container.id} Rendering`);

        return(
            <div className={this.state.collapsed ? 'con collapsed' : 'con'}>
                <div className={'con-item columns is-mobile no-gap is-marginless is-paddingless'}>
                    <div className={'item-stat column is-narrow'}>
                        {container.name}
                    </div>
                    <div className={'item-controls column is-narrow'}>
                        <ItemButton icon={this.state.collapsed ? fas.faAngleUp : fas.faAngleDown} fn={this.collapse} />
                    </div>
                    <div className={'item-stat warning column has-text-right'}>
                        {this.state.contents_weight} | {container.capacity}
                    </div>
                    <ItemControls/>
                </div>
                <div className={'container-contents'}>
                    {
                        Object.keys(container.contents).map( key => {
                            let item = container.contents[key];
                            if (item.type === 'Container' || item.type === 'MagicContainer'){
                                return(<Container container={item} key={key} />)
                            } else {
                                return(
                                    <Item id={item.id} name={item.name} quantity={item.quantity} key={key} />
                                )
                            }
                        } )
                    }
                </div>
            </div>
        )
    }
}

Container.propTypes = {
    container: PropTypes.objectOf(
        PropTypes.shape({
            id: PropTypes.string,
            name: PropTypes.string,
            type: PropTypes.string,
            capacity: PropTypes.number,
            quantity: PropTypes.number,
            value: PropTypes.number,
            weight: PropTypes.number,
            contents: PropTypes.object
        })
    )
};

class ConnectedInventory extends Component {
    constructor(props){
        super(props);

        console.log(this.props.data);
    }

    render(){
        return(
            <Grid>
                {Object.keys(this.props.data).map( key => <Container container={this.props.data[key]} key={key}/> )}
            </Grid>
        )
    }
}

const Inventory = connect(map_state_to_inventory)(ConnectedInventory);
export default Inventory;
