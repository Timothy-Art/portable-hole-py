import React, { Component } from 'react';
import { connect } from 'react-redux';
import store from '../store';

const map_dispatch_to_controls = dispatch => ({

});


class ConnectedControlStrip extends Component{
    constructor(props){
        super(props);
    }

    render(){
        return(
            <nav className={'level has-background-white'}>
                <div className={'level-item has-text-centered'}>
                    <div className={'item-controls column is-narrow has-text-right'}>
                        <a className={'item-btn'}>
                            Add
                        </a>
                    </div>
                </div>
            </nav>
        )
    }
}

const ControlStrip = connect(null, map_dispatch_to_controls)(ConnectedControlStrip);

export default ControlStrip;
