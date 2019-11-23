import React from 'react';

import BrowserRouter from "react-router-dom";
import Routes from './routing';

import store from './store';
import Provider from "react-redux";

import './App.css';

function App() {
  return (
      <Provider store={store}>
          <BrowserRouter>
              <div className="App">
                  <Routes/>
              </div>
          </BrowserRouter>
      </Provider>
  );
}

export default App;
