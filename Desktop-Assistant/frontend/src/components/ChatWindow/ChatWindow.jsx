import React from 'react'

import ChatMessage from '../ChatMessage/ChatMessage'

import "./ChatWindow.css"

const ChatWindow = ({ messages }) => {
  return (
    <div className={messages.length > 0 ? "window-container" : ""}>
      <div className="message-container">
        {
          messages.map((msgObj, index) => {
            return <ChatMessage 
              key={index} 
              role={msgObj.role} 
              text={msgObj.text}
            />  
          })
        }
      </div>
    </div>
  )
}

export default ChatWindow