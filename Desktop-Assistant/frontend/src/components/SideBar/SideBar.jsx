import React from 'react'

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faBars, faGear } from "@fortawesome/free-solid-svg-icons"
import { faPenToSquare } from '@fortawesome/free-regular-svg-icons'

import "./SideBar.css"

const SideBar = () => {
  return (
    <div className="sidebar-container">
      <div className="sidebar-top">
        <FontAwesomeIcon icon={faBars} className="icon hover"/>
        <FontAwesomeIcon icon={faPenToSquare} className="icon hover"/>
      </div>

      <div className="sidebar-bottom">
        <FontAwesomeIcon icon={faGear} className="icon hover"/>
      </div>
    </div>
  )
}

export default SideBar