import { useState } from 'react';
import SideBar from './SideBar';
import './MainLayout.css';

/**
 * Layout principal que contiene el sidebar y el contenido principal
 * @param {Object} props - Propiedades del componente
 * @param {React.ReactNode} props.children - Contenido a renderizar dentro del layout
 */
function MainLayout({ children }) {
  // Estado para controlar si el sidebar está abierto o cerrado
  const [sidebarOpen, setSidebarOpen] = useState(false);
  
  // Función para alternar el estado del sidebar
  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };
  
  return (
    <div className={`layout-container ${sidebarOpen ? 'sidebar-open' : ''}`}>
      {/* Botón para mostrar/ocultar sidebar */}
      <button 
        className="sidebar-toggle"
        onClick={toggleSidebar}
        aria-label={sidebarOpen ? "Cerrar menú" : "Abrir menú"}
      >
        {sidebarOpen ? '←' : '→'}
      </button>
      
      {/* Sidebar con parámetro de visibilidad */}
      <SideBar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      
      {/* Contenido principal */}
      <main className="main-content">
        {children}
      </main>
    </div>
  );
}

export default MainLayout;