import React from 'react';
import './Header.css';

const Header = () => (
  <div className="Header">
      <div className="jumbotron">
          <h1 className="text-center">CSLE Monitoring System</h1>
          <span className="subtitle">
              CSLE (Cyber Security Learning Environment)
              is a platform for building self-learning systems for cyber security using a reinforcement learning approach</span>
      </div>
  </div>
);

Header.propTypes = {};

Header.defaultProps = {};

export default Header;
