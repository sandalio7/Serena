import { useState } from 'react';
import SideBar from './SideBar';
import './MainLayout.css';

function MainLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  
  console.log("MainLayout render, sidebar open:", sidebarOpen);
  
  const toggleSidebar = () => {
    console.log("Toggling sidebar from", sidebarOpen, "to", !sidebarOpen);
    setSidebarOpen(!sidebarOpen);
  };
  
  return (
    <div className={`layout-container ${sidebarOpen ? 'sidebar-open' : ''}`}>
      <button 
        className="sidebar-toggle"
        onClick={toggleSidebar}
        aria-label={sidebarOpen ? "Cerrar menú" : "Abrir menú"}
      >
        {sidebarOpen ? '←' : '→'}
      </button>
      
      <SideBar 
        isOpen={sidebarOpen} 
        onClose={() => {
          console.log("Closing sidebar from SideBar component");
          setSidebarOpen(false);
        }} 
      />
      
      <main className="main-content">
        {children}
      </main>
    </div>
  );
}

export default MainLayout;