import React from 'react';
import './Header.css';

const Header = () => (
  <div className="Header">
      <div className="jumbotron">
          <h1 className="text-center">PyCr ANIP: Automated Network Intrusion Prevention </h1>
          <span className="subtitle">PyCr is a Cyber Range for Reinforcement Learning Agents</span>
      </div>
  </div>
);

Header.propTypes = {};

Header.defaultProps = {};

export default Header;
