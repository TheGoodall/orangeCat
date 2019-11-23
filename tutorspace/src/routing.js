import React from 'react';
import {Switch, Route, Redirect, withRouter} from 'react-router-dom';
import {connect} from 'react-redux';

const Routes = ({logged_in}) => (
    logged_in ? (
        <Switch>
            <Route exact path='/'>
                <Redirect to='/home'/>
            </Route>
            <Route path='/home'>
                Welcome home!
            </Route>
            <Route>
                404 Page not found!
            </Route>
        </Switch>
    ) : (
        <Switch>
            <Route exact path='/'/>
            <Route path='/login'/>
            <Route>
                404 Page not found!
            </Route>
        </Switch>
    )
);

export default withRouter(connect(
    ({logged_in}) => ({logged_in})
)(Routes));