import React from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDiamond } from "@fortawesome/free-solid-svg-icons";

import "./ChatMessage.css";

const ChatMessage = ({ role, text }) => {
  return (
    <div className="message">
      <div className={role === "user" ? "user" : "assistant"}>
        {role === "assistant" && (
          <div className="icon-container">
            <div className="icon">
              <FontAwesomeIcon
                icon={faDiamond}
                style={{ color: "rgb(0, 136, 255)" }}
              />
            </div>
          </div>
        )}
        <div className="text">{text}</div>
      </div>
    </div>
  );
};

export default ChatMessage;
