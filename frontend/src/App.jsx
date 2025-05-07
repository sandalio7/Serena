import { useState } from 'react';
import './App.css';
import MainLayout from './components/layout/MainLayout';
import EconomicDashboard from './pages/EconomicDashboard';

function App() {
  // Este estado temporal será reemplazado cuando implementemos la navegación real
  const [currentPage, setCurrentPage] = useState('economic');

  return (
    <MainLayout>
      {/* Por ahora solo mostramos el dashboard económico */}
      {currentPage === 'economic' && <EconomicDashboard />}
    </MainLayout>
  );
}

export default App;