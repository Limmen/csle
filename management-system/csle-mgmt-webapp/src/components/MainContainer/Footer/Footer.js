import React from 'react';
import './Footer.css';
import CDISLogo from "./cdis_logo.png";
import KTHLogo from "./kth_logo.png";

/**
 * The footer component that is present on every page
 */
const Footer = () => (
  <div className="Footer">
      <footer className="footer">
          <div className="container">
              <p className="text-muted">Released under the Creative Commons Attribution-ShareAlike 4.0 International License
                  <a href={"https://github.com/Limmen/csle"} className="githubLink">
                      <i className="fa fa-github" aria-hidden="true"/>
                  </a>
              </p>
              <p className="text-muted">Copyright 2020-2025@Kim Hammar</p>
              <img src={CDISLogo} alt="CDIS" width={40} height={40}/>
              <img src={KTHLogo} alt="KTH" width={40} height={40} className="kthLogo"/>
          </div>
      </footer>
  </div>
);

Footer.propTypes = {};
Footer.defaultProps = {};
export default Footer;
