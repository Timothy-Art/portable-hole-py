import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { add_item } from "../actions";
import { is_container } from "../inventory-mgmt";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import * as fas from '@fortawesome/pro-solid-svg-icons';
import './css/control-strip.css';

const map_state_to_controls = state => ({
    items: state.items,
    containers: Object.keys(state.data).filter( key => (is_container(state.data[key])) )
});

const map_dispatch_to_controls = dispatch => ({
    add_item: ( id, item ) => dispatch(add_item(id, item))
});

const NameInputs = ({ items, selected, set_selection, name, set_name }) => (
    <div className={'columns is-centered'}>
        <div className={'column'}>
            <label className={'has-text-light'}>Item:</label>
            <div className={'field has-addons has-addons-centered'}>
            <div className={'control'}>
                <div className={'select'}>
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
    </div>
);

const LocationInput = ({ containers, location, set_location }) => (
    <div className={'columns is-centered'}>
        <div className={'column'}>
            <label className={'has-text-light'}>Store in:</label>
            <div className={'field is-grouped is-grouped-centered'}>
            <div className={'control'}>
                <div className={'select'}>
                    <select value={location} onChange={set_location}>
                        {containers.map((item, key) => <option key={key} value={key}>{item}</option>)}
                    </select>
                </div>
            </div>
            </div>
        </div>
    </div>
);

const DetailInputs = ({}) => (
    <div className={'columns is-centered'}>
        <div className={'column'}>
            Details
        </div>
    </div>
);


class AddForm extends Component{
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
            quantity: 0,
            location: 0,
            details: false,
            type: '',
            weight: 0,
            value: 0,
            magic: false,
            container: false,
            capacity: 0
        }
    }

    constructor(props){
        super(props);

        this.state = AddForm.default_state();
        this.reset = this.reset.bind(this);
        this.set_name = this.set_name.bind(this);
        this.set_selection = this.set_selection.bind(this);
        this.set_location = this.set_location.bind(this);
    }

    reset(){
        this.setState(AddForm.default_state());
        this.props.close()
    }

    set_name(event){
        console.log(event);
        this.setState({selected: 0, name: event.target.value, details: true});
    }

    set_selection(event){
        this.setState({selected: event.value, name: '', details: false});
    }

    set_location(event){
        this.setState({location: event.value});
    }

    render(){
        let items = Array({name: 'Select'}, ...this.props.items);

        return(
            <div className={'add-dialog ' + this.props.active}>
                <div className={'container dialog'} onClick={(event) => event.stopPropagation()}>
                    <div className={'columns is-centered is-mobile'}>
                        <div className={'column is-one-fifth'}>
                            <a className={'add-cross button is-black is-inverted is-outlined'} onClick={this.reset}>
                                <FontAwesomeIcon icon={fas.faTimes} style={{width: '24px', height: '24px'}}/>
                            </a>
                        </div>
                    </div>

                    <hr className={'form-break'} />
                    <NameInputs
                        items={items}
                        selected={this.state.selected}
                        set_selection={this.set_selection}
                        name={this.state.name}
                        set_name={this.set_name}
                    />
                    <LocationInput
                        containers={this.props.containers}
                        location={this.state.location}
                        set_location={this.set_location}
                    />
                    { this.state.details ? <DetailInputs /> : null}
                    <hr className={'form-break'} />

                    <div className={'columns is-centered is-mobile'}>
                        <div className={'column is-one-fifth'}>
                            <a className={'button is-fullwidth'} onClick={this.props.submit}>Add</a>
                        </div>
                        <div className={'column is-one-fifth'}>
                            <a className={'button is-fullwidth is-danger'} onClick={this.reset}>Cancel</a>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

class AddButton extends Component{
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


class ConnectedControlStrip extends Component{
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
