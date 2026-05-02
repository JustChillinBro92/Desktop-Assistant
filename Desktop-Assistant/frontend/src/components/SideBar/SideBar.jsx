import React from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars, faGear } from "@fortawesome/free-solid-svg-icons";
import { faPenToSquare } from "@fortawesome/free-regular-svg-icons";

import "./SideBar.css";

const SideBar = () => {
  return (
    <div className="sidebar-container">
      <div className="sidebar-top">
        <div className="icon hover">
          <FontAwesomeIcon icon={faBars} />
        </div>
        <div className="icon hover">
          <FontAwesomeIcon icon={faPenToSquare} />
        </div>
      </div>

      <div className="sidebar-bottom">
        <div className="icon hover">
          <FontAwesomeIcon icon={faGear} />
        </div>
      </div>
    </div>
  );
};

export default SideBar;
