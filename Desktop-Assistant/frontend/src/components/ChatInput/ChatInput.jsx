import React from 'react'
import { useEffect } from 'react';
import { useState } from 'react'

const ChatInput = ({ handleSend }) => {
  const [userInput, setUserInput] = useState("");

  const onChangeHandler = (e) => {
    setUserInput(e.target.value);
  }

  const onSendHandler = () => {
    if(!userInput.trim()) return; // empty input
    handleSend(userInput);
    setUserInput("");
  }

  // useEffect(()=>{
  //   console.log(input);
  // },[input])

  return (
    <div className="input-container">
      <div className="text-box">
        <input 
          type="text" 
          value={userInput}
          onChange={onChangeHandler}
          placeholder="Ask anything"
        />
      </div>
      <button onClick={onSendHandler}>Send</button>
    </div>
  )
}

export default ChatInput