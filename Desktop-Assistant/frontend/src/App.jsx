import React from 'react'
import { Routes, Route } from "react-router-dom";

import { sendMessage } from './api/assistant_api'

import Home from './pages/Home/Home';

import "./index.css"

const App = () => {
  return (
    <div className="page">
      <div className="app">
        <div className="app-content">
          <Routes>
            <Route path="/" element={<Home/>}/>
          </Routes>
        </div>
      </div>
    </div>
  )
}

export default App