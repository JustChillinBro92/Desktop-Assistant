import React, { useEffect, useRef, useState } from "react";

import { sendMessage } from "../../api/assistant_api";

import Navbar from "../../components/Navbar/Navbar";
import SideBar from "../../components/SideBar/SideBar";
import ChatWindow from "../../components/ChatWindow/ChatWindow";
import ChatInput from "../../components/ChatInput/ChatInput";

import "./Home.css";

const Home = () => {
  const [hamburgerClick, setHamburgerClick] = useState(false);
  const [messages, setMessages] = useState([]); // store chat history
  const messagesRef = useRef(null);

  const handleSend = async (userInput) => {
    // add user message to previous chat state
    setMessages((prev) => [...prev, { role: "user", text: userInput }]);

    // call backend api
    const aiResonse = await sendMessage(userInput);

    // add ai response to previous chat state
    setMessages((prev) => [
      ...prev,
      { role: "assistant", text: aiResonse.message || "No response!" },
    ]);
  };

  // reset chat history on page refresh
  useEffect(() => {
    fetch("http://localhost:8000/new-chat", {
      method: "POST",
    });
  },[]);

  // auto scroll to end of page
  useEffect(() => {
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="home-container">
      <SideBar 
        setMessages={setMessages} 
        hamburgerClick={hamburgerClick}
        setHamburgerClick={setHamburgerClick}
      />
      <div className="home-middle">
        <Navbar 
          hamburgerClick={hamburgerClick}
          setHamburgerClick={setHamburgerClick}
        />

        <div className={messages.length === 0 ? "header" : "header-chat-active"}>
          <div className="welcome-msg">
            <h2>Hi JustChillinBro</h2>
            <h1>How can I help you today?</h1>
          </div>
        </div>

        <div className="content">
          <div ref={messagesRef}
            className={messages.length === 0 ? "" : "messages-chat-active"}>
            <ChatWindow messages={messages} />
          </div>
          <div className={messages.length === 0 ? "" : "input-chat-active"}>
            <ChatInput handleSend={handleSend} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
