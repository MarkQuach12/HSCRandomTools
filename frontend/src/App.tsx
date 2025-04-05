import { useState } from 'react'
import './App.css'
import Predict from './components/pages/Predict'
import Band6 from './components/pages/Band6'
import Navbar from './components/pages/Navbar'
import { Routes, Route } from 'react-router-dom';

function App() {
  return (
    <div className="pt-20 px-4">
    <Navbar />
      <Routes>
        <Route path="/"/>
        <Route path="/predict" element={<Predict />} />
        <Route path="/band6" element={<Band6 />} />
      </Routes>
    </div>
  )
}

export default App
