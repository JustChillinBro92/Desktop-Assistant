import React from 'react'

const ChatMessage = ({ role, text }) => {
  return (
    <div className="message">
      {role === "user" ? "You" : "Assistant"}: {text}
    </div>
  )
}

export default ChatMessage