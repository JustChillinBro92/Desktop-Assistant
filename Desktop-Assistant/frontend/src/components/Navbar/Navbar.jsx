import React, { useState } from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars, faGear } from "@fortawesome/free-solid-svg-icons";

import "./Navbar.css";

const Navbar = ({ hamburgerClick, setHamburgerClick }) => {
  const handleHamburgerClick = () => {
    setHamburgerClick(!hamburgerClick);
  }

  return (
    <div className="navbar-container">
      <div className="contents">
        <div className="app-name-container">
          <div className="hamburger">
            <div className="icon hover">
              <FontAwesomeIcon icon={faBars} 
                onClick={handleHamburgerClick}
              />
            </div>
          </div>
          <div className="app-name">
            <h1>Luna</h1>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Navbar;
