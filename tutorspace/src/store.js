import {createStore} from "redux";

const default_state = {
    logged_in: false
};

const reducer = (state = default_state, action) => ({state});

export default createStore(reducer, window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__());