import { useState } from 'react'
import './App.css'
import Predict from './components/pages/Predict'
import Band6 from './components/pages/Band6'
import { Routes, Route } from 'react-router-dom';

function App() {
  return (
      <Routes>
        <Route path="/" element={<div>Home</div>} />
        <Route path="/predict" element={<Predict />} />
        <Route path="/band6" element={<Band6 />} />
      </Routes>
  )
}

export default App
