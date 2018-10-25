import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { add_item } from "../actions";
import { is_container, pretty_id } from "../inventory-mgmt";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { fromJS } from 'immutable';
import { CONTAINERS, MAGIC } from "../constants/types";
import * as fas from '@fortawesome/pro-solid-svg-icons';
import './css/control-strip.css';

const map_state_to_controls = state => ({
    items: state.get('items').toJS(),
    containers: [... state.get('data').filter( val => (is_container(val.toJS())) ).keys()]
});

const map_dispatch_to_controls = dispatch => ({
    add_item: ( id, item ) => dispatch(add_item(id, item))
});

const NameInputs = ({ items, selected, set_selection, name, set_name }) => {
    return (
        <div className={'span-full'}>
            <label className={'has-text-light'}>Item:</label>
            <div className={'field has-addons has-addons-centered'}>
                <div className={'control is-expanded'}>
                    <div className={'select is-fullwidth'}>
                        <select value={selected} onChange={set_selection}>
                            {items.map((item, key) => <option key={key} value={key}>{item.name}</option>)}
                        </select>
                    </div>
                </div>
                <div className={'control'}>
                    <span className={'button is-static'}>or</span>
                </div>
                <div className={'control'}>
                    <input type={'text'} className={'input'} value={name} onChange={set_name} placeholder={'Add new item'}/>
                </div>
            </div>
        </div>
    )
};

const QuantityInput = ({ quantity, set_quantity, inc_quantity }) => {
    return (
        <div>
            <label className={'has-text-light'}> Quantity: </label>
            <div className={'field has-addons has-addons-centered'}>
                <div className={'control'}>
                    <button className={'button is-danger'} onClick={() => inc_quantity(-1)} >
                        <FontAwesomeIcon icon={fas.faMinus} />
                    </button>
                </div>
                <div className={'control'}>
                    <input
                        className={'input has-text-centered'}
                        type={'number'}
                        value={quantity}
                        min={1}
                        onChange={set_quantity}
                    />
                </div>
                <div className={'control'}>
                    <button className={'button is-danger'} onClick={() => inc_quantity(+1)}>
                        <FontAwesomeIcon icon={fas.faPlus} />
                    </button>
                </div>
            </div>
        </div>
    )
};

const LocationInput = ({ containers, location, set_location }) => {
    return(
        <div>
            <label className={'has-text-light'}>Store in:</label>
            <div className={'control is-expanded'}>
                <div className={'select is-fullwidth'}>
                    <select value={location} onChange={set_location}>
                        {containers.map((item, key) => <option key={key} value={key}>{pretty_id(item)}</option>)}
                    </select>
                </div>
            </div>
        </div>
    );
};

const DetailInputs = (props) => {
    return(
        <div className={'grid-dialog span-full'}>
            <div className={'span-full'}>
                <label className={'has-text-light'}>Details:</label>
            </div>
            <div className={'span-full'}>
                <label className={'has-text-light'}>Type:</label>
                <div className={props.container ? 'field has-addons' : 'field'}>
                    <div className={'control is-expanded'}>
                        <div className={'select is-fullwidth'}>
                            <select value={props.type} onChange={props.set_type}>
                                <option value={'Item'}>Item</option>
                                <option value={'MagicItem'}>Magic Item</option>
                                <option value={'Container'}>Container</option>
                                <option value={'MagicContainer'}>Magic Container</option>
                                <option value={'Player'}>Player</option>
                                <option value={'Location'}>Location</option>
                            </select>
                        </div>
                    </div>
                    {props.container ? (
                        <div className={'control'}>
                            <input className={'input'} type={'number'} value={props.capacity} placeholder={'Capacity'}
                                   onChange={props.set_capacity}/>
                        </div>
                    ) : null}
                </div>
            </div>
            <div className={'has-text-centered'}>
                <label className={'has-text-light'}>Value:</label>
                <div>
                    <input className={'input'} type={'number'} value={props.value} onChange={props.set_value}/>
                </div>
            </div>
            <div className={'has-text-centered'}>
                <label className={'has-text-light'}>Weight:</label>
                <div>
                    <input className={'input'} type={'number'} value={props.weight} onChange={props.set_weight}/>
                </div>
            </div>
        </div>
    )
};

class AddForm extends PureComponent{
    static propTypes = {
        active: PropTypes.bool.isRequired,
        close: PropTypes.func.isRequired,
        submit: PropTypes.func.isRequired,
        containers: PropTypes.array.isRequired,
        items: PropTypes.array.isRequired
    };


    static default_state(){
        return {
            name: '',
            selected: 0,
            quantity: 1,
            location: 0,
            details: false,
            type: '',
            weight: 0,
            value: 0,
            magic: false,
            container: false,
            capacity: ''
        }
    }

    constructor(props){
        super(props);

        this.state = AddForm.default_state();

        this.reset = this.reset.bind(this);
        this.submit = this.submit.bind(this);

        this.set_name = this.set_name.bind(this);
        this.set_selection = this.set_selection.bind(this);
        this.set_location = this.set_location.bind(this);
        this.set_type = this.set_type.bind(this);
        this.set_capacity = this.set_capacity.bind(this);
        this.set_value = this.set_value.bind(this);
        this.set_weight = this.set_weight.bind(this);
        this.set_quantity = this.set_quantity.bind(this);
        this.inc_quantity = this.inc_quantity.bind(this);
    }

    submit(){

    }

    reset(){
        this.setState(AddForm.default_state());
        this.props.close()
    }

    set_name(event){
        this.setState({selected: 0, name: event.target.value, details: true});
    }

    set_selection(event){
        let selected = parseInt(event.target.value);
        let item = fromJS(this.props.items[selected - 1]);
        let container = is_container(item);

        let new_state = Object.assign(item.toJS(), {selected: selected, details: false, container: container});

        console.log(new_state);

        this.setState(new_state);
    }

    set_location(event){
        this.setState({location: event.target.value});
    }

    set_type(event){
        let container = false;
        let magic = false;
        if (CONTAINERS.has(event.target.value)){
            container = true;
        }
        if (MAGIC.has(event.target.value)){
            magic = true;
        }

        this.setState({type: event.target.value, container: container, magic: magic});
    }

    set_capacity(event){
        this.setState({capacity: event.target.value});
    }

    set_weight(event){
        this.setState({weight: event.target.value});
    }

    set_value(event){
        this.setState({value: event.target.value});
    }

    set_quantity(event){
        let quantity = parseInt(event.target.value);
        if (isNaN(quantity)){
            quantity = '';
        }
        this.setState({quantity: quantity});
    }

    inc_quantity(x){
        let quantity = Math.max(this.state.quantity + x, 1);
        this.setState({quantity: quantity})
    }

    render(){
        let items = Array({name: 'Select'}, ...this.props.items);

        return(
            <div className={'add-dialog ' + this.props.active}>
                <div className={'dialog'} onClick={(event) => event.stopPropagation()}>
                    <div className={'grid-dialog'}>

                        <a className={'add-cross span-full button is-dark is-inverted is-outlined'} onClick={this.reset}>
                            <FontAwesomeIcon icon={fas.faTimes} style={{width: '24px', height: '24px'}}/>
                        </a>

                        <NameInputs
                            items={items}
                            selected={this.state.selected}
                            set_selection={this.set_selection}
                            name={this.state.name}
                            set_name={this.set_name}
                        />
                        <QuantityInput
                            quantity={this.state.quantity}
                            set_quantity={this.set_quantity}
                            inc_quantity={this.inc_quantity}
                        />
                        <LocationInput
                            containers={this.props.containers}
                            location={this.state.location}
                            set_location={this.set_location}
                        />
                        { this.state.details ? <DetailInputs
                            type={this.state.type}
                            set_type={this.set_type}
                            container={this.state.container}
                            capacity={this.state.capacity}
                            set_capacity={this.set_capacity}
                            weight={this.state.weight}
                            set_weight={this.set_weight}
                            value={this.state.value}
                            set_value={this.set_value}
                            quantity={this.state.quantity}
                            set_quantity={this.set_quantity}
                        /> : null}
                        <div className={'span-full'}/>
                        <a className={'button is-fullwidth'} onClick={this.props.submit}>Add</a>
                        <a className={'button is-fullwidth is-danger'} onClick={this.reset}>Cancel</a>
                    </div>
                </div>
            </div>
        );
    }
}

class AddButton extends PureComponent{
    static propTypes = {
        containers: PropTypes.array.isRequired,
        items: PropTypes.array.isRequired
    };

    constructor(props){
        super(props);

        this.state = {
            active: false
        };

        this.open_dialog = this.open_dialog.bind(this);
        this.close_dialog = this.close_dialog.bind(this);
    }

    open_dialog(){
        this.setState({active: true});
    }

    close_dialog(){
        this.setState({active: false});
    }

    render(){
        return(
            <div>
                <div className={'item-controls'}>
                    <a className={'button'} onClick={this.open_dialog}>
                        Add
                    </a>
                </div>
                <AddForm
                    active={this.state.active}
                    submit={()=>(null)}
                    close={this.close_dialog}
                    containers={this.props.containers}
                    items={this.props.items}
                />
            </div>
        )
    }
}

class ConnectedControlStrip extends PureComponent{
    static propTypes = {
        containers: PropTypes.array.isRequired,
        items: PropTypes.array.isRequired
    };

    constructor(props){
        super(props);
        console.log(props.containers);
    }

    render(){
        return(
            <div>
                <nav className={'level has-background-white control-strip'}>
                    <div className={'level-item has-text-centered'}>
                        <AddButton containers={this.props.containers} items={this.props.items} />
                    </div>
                </nav>
                <div className={'control-spacing'} />
            </div>
        )
    }
}

const ControlStrip = connect(map_state_to_controls, map_dispatch_to_controls)(ConnectedControlStrip);

export default ControlStrip;
