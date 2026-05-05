import { useRef, useEffect } from "react";
import { useState } from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";

import "./ChatInput.css";

const ChatInput = ({ handleSend }) => {
  const [userInput, setUserInput] = useState("");
  const textareaRef = useRef(null);

  const onChangeHandler = (e) => {
    setUserInput(e.target.value);

    const el = textareaRef.current;
    el.style.height = "auto";
    el.style.height = el.scrollHeight + "px";
  };

  const onSendHandler = () => {
    if (!userInput.trim()) return; // empty input
    handleSend(userInput);
    setUserInput("");

    const el = textareaRef.current;
    el.style.height = "auto";
  };

  const onEnterPressHandler = (e) => {
    if(e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSendHandler();
    }
  }

  return (
    <div className="input-container">
      <div className="text-box-container">
        <div className="text-box">
          <textarea
            type="text"
            ref={textareaRef}
            value={userInput}
            onChange={onChangeHandler}
            onKeyDown={onEnterPressHandler}
            placeholder="Ask anything"
            rows={1}
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
