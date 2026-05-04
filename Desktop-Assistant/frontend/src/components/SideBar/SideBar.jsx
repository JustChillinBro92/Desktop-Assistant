import React, { use, useEffect } from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars, faGear } from "@fortawesome/free-solid-svg-icons";
import { faPenToSquare, faCircleXmark } from "@fortawesome/free-regular-svg-icons";

import "./SideBar.css";

const SideBar = ({ setMessages, hamburgerClick, setHamburgerClick }) => {
  const handleNewChat = () => {
    setMessages([]);
  }

  const handleClick = (category) => {
    switch(category) {
      case "cross":
        setHamburgerClick(!hamburgerClick)
        break;
    }
  }

  return (
    <div className={!hamburgerClick ? "sidebar-container" : "sidebar-container-overlay"}>
      <div className={hamburgerClick ? "active-cross hover" : "inactive-cross"}
        onClick={()=>handleClick("cross")}>
        <FontAwesomeIcon icon={faCircleXmark} />
      </div>

      <div className="sidebar-top">
        <div className={!hamburgerClick? "icon hover" : "hamburger"}>
          <FontAwesomeIcon icon={faBars} />
        </div>

        <div className="icon hover" onClick={handleNewChat}>
          <FontAwesomeIcon icon={faPenToSquare} />
          {hamburgerClick && <span>New Chat</span>}
        </div>

      </div>

      <div className="sidebar-bottom">
        <div className="icon hover">
          <FontAwesomeIcon icon={faGear} />
          {hamburgerClick && <span>Settings</span>}
        </div>
      </div>
      
    </div>
  );
};

export default SideBar;
