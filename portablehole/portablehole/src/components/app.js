import React, { Component } from "react";
import Inventory from './inventory';
import ControlStrip from './control-strip';

class App extends Component {
    render() {
        return (
            <div className="App">
                <ControlStrip />
                <Inventory />
            </div>
        );
      }
}

export default App;
