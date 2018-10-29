import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { add_item } from "../actions";
import { create_id, is_container, pretty_id, get_id } from "../inventory-mgmt";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { fromJS } from 'immutable';
import { CONTAINERS, MAGIC, STANDALONE } from "../constants/types";
import * as fas from '@fortawesome/pro-solid-svg-icons';
import './css/control-strip.css';

const map_state_to_controls = state => ({
    items: state.get('items').toJS(),
    containers: ['-', ... state.get('data').filter( val => (is_container(val.toJS())) ).keys()]
});

const map_dispatch_to_controls = dispatch => ({
    add_item: ( id, item ) => dispatch(add_item(id, item))
});

const NameInputs = ({ items, selected, set_selection, name, set_name, valid }) => {
    return (
        <div className={'span-full'}>
            <label className={'has-text-light'}>Item:</label>
            <div className={'field has-addons has-addons-centered'}>
                <div className={'control is-expanded'}>
                    <div className={valid ? 'select is-fullwidth' : 'select is-fullwidth is-danger'}>
                        <select value={selected} onChange={set_selection}>
                            {items.map((item, key) => <option key={key} value={key}>{item.name}</option>)}
                        </select>
                    </div>
                </div>
                <div className={'control'}>
                    <span className={'button is-static'}>or</span>
                </div>
                <div className={'control'}>
                    <input type={'text'} className={valid ? 'input' : 'input is-danger has-text-danger'} value={name} onChange={set_name} placeholder={'Add new item'}/>
                </div>
            </div>
            {valid ? null : <p className="help is-danger">Item not set!</p>}
        </div>
    )
};

const QuantityInput = ({ quantity, set_quantity, inc_quantity, valid }) => {
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
                        className={valid ? 'input has-text-centered' : 'input has-text-centered is-danger has-text-danger'}
                        type={'number'}
                        value={quantity}
                        min={1}
                        onChange={set_quantity}
                    />
                    {valid ? null : <p className="help is-danger">Invalid quantity!</p>}
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

const DetailInputs = props => {
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
                            <input
                                className={props.capacity_valid ? 'input' : 'input is-danger has-text-danger'}
                                type={'number'}
                                value={props.capacity}
                                placeholder={'Capacity'}
                                onChange={props.set_capacity}
                            />
                            {props.capacity_valid ? null : <p className="help is-danger">Invalid capacity!</p>}
                        </div>
                    ) : null}
                </div>
            </div>
            {!props.standalone ? (
                <div className={'has-text-centered'}>
                    <label className={'has-text-light'}>Value:</label>
                    <div>
                        <input
                            className={props.value_valid ? 'input' : 'input is-danger has-text-danger'}
                            type={'number'}
                            value={props.value}
                            onChange={props.set_value}
                        />
                        {props.value_valid ? null : <p className="help is-danger">Invalid value!</p>}
                    </div>
                </div>
            ) : null}
            {!props.standalone ? (
                <div className={'has-text-centered'}>
                    <label className={'has-text-light'}>Weight:</label>
                    <div>
                        <input
                            className={props.weight_valid ? 'input' : 'input is-danger has-text-danger'}
                            type={'number'}
                            value={props.weight}
                            onChange={props.set_weight}
                        />
                        {props.weight_valid ? null : <p className="help is-danger">Invalid weight!</p>}
                    </div>
                </div>
            ) : null}
        </div>
    );
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
            location: 1,
            type: 'Item',
            weight: 0,
            value: 0,
            capacity: '',
            details: false,
            magic: false,
            container: false,
            standalone: false,
            name_valid: false,
            quantity_valid: true,
            weight_valid: true,
            value_valid: true,
            capacity_valid: true
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
        let valid =
            this.state.name_valid &&
            this.state.value_valid &&
            this.state.weight_valid &&
            this.state.capacity_valid &&
            this.state.quantity_valid;

        if (valid){
            let location = this.state.location === 0 ? '' : this.props.containers[this.state.location];
            let id = this.state.details ? get_id(this.state.name) : this.state.name;

            let item = {
                name: this.state.name,
                id: create_id(location, id),
                type: this.state.type,
                capacity: this.state.capacity === '' ? 0 : parseInt(this.state.capacity),
                weight: this.state.weight === '' ? 0 : parseInt(this.state.weight),
                value: this.state.value === '' ? 0.0 : parseFloat(this.state.value),
                quantity: this.state.quantity === '' ? 0.0 : parseFloat(this.state.quantity),
                magic: this.state.magic,
                contents: this.state.container ? [] : undefined
            };
            console.log('submit', item);

            this.props.submit(item.id, item);
            this.reset();
        }
    }

    reset(){
        this.setState(AddForm.default_state());
        this.props.close()
    }

    set_name(event){
        let details = true;
        let name_valid = true;
        if (event.target.value === ''){
            details = false;
            name_valid = false;
        } else if (create_id('', event.target.value) === ''){
            details = false;
            name_valid = false;
        }

        this.setState({selected: 0, name: event.target.value, details: details, name_valid: name_valid});
    }

    set_selection(event){
        let selected = parseInt(event.target.value);
        let new_state = {selected: selected, details: false,};

        if (selected > 0){
            let item = fromJS(this.props.items[selected - 1]);
            let container = is_container(item);

            new_state = Object.assign(item.toJS(), new_state, {container: container, name_valid: true});
        }

        console.log(new_state);

        this.setState(new_state);
    }

    set_location(event){
        let location = parseInt(event.target.value);
        console.log(location);
        if (this.state.standalone){
            location = 0;
        } else if (location === 0){
            location = this.state.location;
        }

        this.setState({location: location});
    }

    set_type(event){
        let container = false;
        let magic = false;
        let standalone = false;
        let location = this.state.location;

        if (CONTAINERS.has(event.target.value)){
            container = true;
        }
        if (MAGIC.has(event.target.value)){
            magic = true;
        }
        if (STANDALONE.has(event.target.value)){
            standalone = true;
            location = 0;
        }

        this.setState({
            location: location,
            type: event.target.value,
            container: container,
            magic: magic,
            standalone: standalone
        });
    }

    set_capacity(event){
        let cap_valid = true;

        try {
            if (parseInt(event.target.value) < 0){
                cap_valid = false;
            }
        } catch (e) {
            cap_valid = false;
        }

        this.setState({capacity: event.target.value, capacity_valid: cap_valid});
    }

    set_weight(event){
        let weight_valid = true;

        try {
            if (parseFloat(event.target.value) < 0){
                weight_valid = false;
            }
        } catch (e) {
            weight_valid = false;
        }

        this.setState({weight: event.target.value, weight_valid: weight_valid});
    }

    set_value(event){
        let value_valid = true;

        try {
            if (parseFloat(event.target.value) < 0){
                value_valid = false;
            }
        } catch (e) {
            value_valid = false;
        }

        this.setState({value: event.target.value, value_valid: value_valid});
    }

    set_quantity(event){
        let quantity_valid = true;
        let quantity = parseInt(event.target.value);
        if (isNaN(quantity)){
            quantity = '';
            quantity_valid = false;
        } else if (quantity < 1){
            quantity_valid = false;
        }

        this.setState({quantity: quantity, quantity_valid: quantity_valid});
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
                            valid={this.state.name_valid}
                        />
                        <QuantityInput
                            quantity={this.state.quantity}
                            set_quantity={this.set_quantity}
                            inc_quantity={this.inc_quantity}
                            valid={this.state.quantity_valid}
                        />
                        <LocationInput
                            containers={this.props.containers}
                            location={this.state.location}
                            set_location={this.set_location}
                        />
                        { this.state.details ? <DetailInputs
                            type={this.state.type}
                            set_type={this.set_type}
                            standalone={this.state.standalone}
                            container={this.state.container}
                            capacity={this.state.capacity}
                            set_capacity={this.set_capacity}
                            capacity_valid={this.state.capacity_valid}
                            weight={this.state.weight}
                            set_weight={this.set_weight}
                            weight_valid={this.state.weight_valid}
                            value={this.state.value}
                            set_value={this.set_value}
                            value_valid={this.state.value_valid}
                            quantity={this.state.quantity}
                            set_quantity={this.set_quantity}
                            quantity_valid={this.state.quantity_valid}
                        /> : null}
                        <div className={'span-full'}/>
                        <a className={'button is-fullwidth'} onClick={this.submit}>Add</a>
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
        items: PropTypes.array.isRequired,
        submit: PropTypes.func
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
                    submit={this.props.submit}
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
        items: PropTypes.array.isRequired,
        add_item: PropTypes.func.isRequired
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
                        <AddButton
                            containers={this.props.containers}
                            items={this.props.items}
                            submit={this.props.add_item}
                        />
                    </div>
                </nav>
                <div className={'control-spacing'} />
            </div>
        )
    }
}

const ControlStrip = connect(map_state_to_controls, map_dispatch_to_controls)(ConnectedControlStrip);

export default ControlStrip;
