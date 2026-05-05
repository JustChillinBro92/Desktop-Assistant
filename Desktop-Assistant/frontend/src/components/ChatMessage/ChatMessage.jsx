import { useEffect, useState } from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDiamond } from "@fortawesome/free-solid-svg-icons";

import "./ChatMessage.css";

const ChatMessage = ({ role, text }) => {
  const [visibleText, setVisibleText] = useState("");

  useEffect(() => {
    let i = 0;

    const interval = setInterval(() => {
      setVisibleText(text.slice(0, i + 1));
      i++;

      if(i === text.length) clearInterval(interval);
    }, 5);

    return () => clearInterval(interval);
  },[text])

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
        {role === "assistant" ? (
          <div className="text">{visibleText}</div>
        ) : (
          <div className="text">{text}</div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
