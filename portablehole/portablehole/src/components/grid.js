import React from 'react';
import './css/grid.css';

const Grid = props => (
    <div className={'grid-container'}>
        { props.children }
    </div>
);

export default Grid;
