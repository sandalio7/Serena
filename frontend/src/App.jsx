import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import './App.css'
import EconomicDashboard from './pages/EconomicDashboard';
import HealthDashboard from './pages/HealthDashboard';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/economic" replace />} />
        <Route path="/economic" element={<EconomicDashboard />} />
        <Route path="/health" element={<HealthDashboard />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App