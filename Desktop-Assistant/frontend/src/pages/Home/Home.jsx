import React from 'react'
import { useState } from 'react'

import { sendMessage } from '../../api/assistant_api'

import ChatWindow from '../../components/ChatWindow/ChatWindow'
import ChatInput from '../../components/ChatInput/ChatInput'


const Home = () => {
  const [messages, setMessages] = useState([]) // store chat history

  const handleSend = async (userInput) => {
    // add user message to previous chat state
    setMessages((prev) => [...prev, { role: "user", text: userInput }]);

    // call backend api
    const aiResonse = await sendMessage(userInput);

    // add ai response to previous chat state
    setMessages((prev) => [...prev, { role: "assistant", text: aiResonse.message || "No response!" }])
  }

  return (
    <div>
      <h2>Welcome! How can help you today?</h2>
      <ChatWindow messages={messages} />
      <ChatInput handleSend={handleSend}/>
    </div>
  )
}

export default Home