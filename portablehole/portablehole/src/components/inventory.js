import React, { Component } from 'react';
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

const Item = ({ item }) => {
    console.log(`${item.id} Rendering`);
    return(
        <div className={'item columns is-mobile no-gap is-marginless is-paddingless'}>
            <div className={'item-stat column is-narrow'}>
                {item.name}
            </div>
            <div className={'item-stat column is-narrow'}>
                {item.quantity > 1 ? 'x' + item.quantity.toFixed(0) : ''}
            </div>
            <div className={'item-controls column has-text-right'}>
                <a className={'btn'}><FontAwesomeIcon icon={fas.faArrowsAlt} fixedWidth={true}/></a>
                <a className={'btn'}><FontAwesomeIcon icon={fas.faUsdCircle} fixedWidth={true}/></a>
                <a className={'btn'}><FontAwesomeIcon icon={fas.faTimes} fixedWidth={true}/></a>
            </div>
        </div>
    )
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
                    <div className={'item-stat column is-narrow'}>
                        {container.quantity > 1 ? 'x' + container.quantity.toFixed(0) : ''}
                    </div>
                    <div className={'item-stat column has-text-right'}>
                        {this.state.contents_weight} | {container.capacity}
                    </div>
                    <div className={'item-controls column is-narrow has-text-right'}>
                        <a className={'btn'} onClick={this.collapse} >
                            <FontAwesomeIcon icon={this.state.collapsed ? fas.faPlus : fas.faMinus} fixedWidth={true}/>
                        </a>
                        <a className={'btn'}><FontAwesomeIcon icon={fas.faArrowsAlt} fixedWidth={true}/></a>
                        <a className={'btn'}><FontAwesomeIcon icon={fas.faUsdCircle} fixedWidth={true}/></a>
                        <a className={'btn'}><FontAwesomeIcon icon={fas.faTimes} fixedWidth={true}/></a>
                    </div>
                </div>
                <div className={'container-contents'}>
                    {
                        Object.keys(container.contents).map( key => {
                            if (container.contents[key].type === 'Container' || container.contents[key].type === 'MagicContainer'){
                                return(<Container container={container.contents[key]} key={key} />)
                            } else {
                                return(<Item item={container.contents[key]} key={key} />)
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
