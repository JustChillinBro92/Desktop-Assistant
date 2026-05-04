import React from "react";
import { useEffect } from "react";
import { useState } from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";

import "./ChatInput.css";

const ChatInput = ({ handleSend }) => {
  const [userInput, setUserInput] = useState("");

  const onChangeHandler = (e) => {
    setUserInput(e.target.value);
  };

  const onSendHandler = () => {
    if (!userInput.trim()) return; // empty input
    handleSend(userInput);
    setUserInput("");
  };

  const onEnterPressHandler = (e) => {
    if(e.key === "Enter")
      onSendHandler();
  }

  return (
    <div className="input-container">
      <div className="text-box-container">
        <div className="text-box">
          <input
            type="text"
            value={userInput}
            onChange={onChangeHandler}
            onKeyDown={onEnterPressHandler}
            placeholder="Ask anything"
          />
        </div>
        <div className="buttons-box">
          <div className="button">
            <FontAwesomeIcon icon={faPaperPlane}
              className="send-btn"
              onClick={onSendHandler}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInput;
