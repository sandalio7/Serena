import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './SideBar.css';

function SideBar({ isOpen, onClose }) {
  const navigate = useNavigate();
  const location = useLocation();
  
  console.log("Current location:", location.pathname);
  console.log("Sidebar is open:", isOpen);
  
  const isActive = (path) => location.pathname === path;
  
  const navigateTo = (path) => {
    console.log("Navigating to:", path);
    navigate(path);
    onClose();
  };

  return (
    <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
      <div className="sidebar-header">
        <h2>Menu</h2>
        <button
          className="close-btn"
          onClick={() => {
            console.log("Close button clicked");
            onClose();
          }}
          aria-label="Cerrar menú"
        >
          ×
        </button>
      </div>
      
      <nav className="sidebar-nav">
        <div 
          className={`nav-item ${isActive('/health') ? 'active' : ''}`}
          onClick={() => navigateTo('/health')}
        >
          <span className="nav-icon">•</span>
          Salud
        </div>
        <div 
          className={`nav-item ${isActive('/economic') ? 'active' : ''}`}
          onClick={() => navigateTo('/economic')}
        >
          <span className="nav-icon">•</span>
          Gastos
        </div>
        <div className="nav-item">
          <span className="nav-icon">•</span>
          Ingresos
        </div>
        <div className="nav-item">
          <span className="nav-icon">•</span>
          Beneficios
        </div>
      </nav>
      
      <div className="user-info">
        <div className="avatar"></div>
        <span className="username">Usuario99</span>
      </div>
    </aside>
  );
}

export default SideBar;