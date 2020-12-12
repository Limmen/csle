import React from 'react';
import PropTypes from 'prop-types';
import './Header.css';

const Header = () => (
  <div className="Header">
      <div className="jumbotron">
          <h1 className="text-center">PyCr Monitor</h1>
          PyCR is a Cyber Range for Reinforcement Learning Agents
      </div>
  </div>
);

Header.propTypes = {};

Header.defaultProps = {};

export default Header;
