import './SideBar.css';

/**
 * Componente de barra lateral
 * @param {Object} props - Propiedades del componente
 * @param {boolean} props.isOpen - Indica si el sidebar está abierto
 * @param {Function} props.onClose - Función para cerrar el sidebar
 */
function SideBar({ isOpen, onClose }) {
  return (
    <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
      <div className="sidebar-header">
        <h2>Menu</h2>
        <button 
          className="close-btn" 
          onClick={onClose}
          aria-label="Cerrar menú"
        >
          ×
        </button>
      </div>
      
      <nav className="sidebar-nav">
        <div className="nav-item">
          <span className="nav-icon">•</span>
          Salud
        </div>
        <div className="nav-item active">
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