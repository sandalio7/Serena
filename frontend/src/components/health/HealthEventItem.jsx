// HealthEventItem.jsx
import React from 'react';
import './HealthEventItem.css';

/**
 * Componente que muestra un elemento individual del historial de salud
 * @param {Object} props - Propiedades del componente
 * @param {Object} props.event - Datos del evento
 * @param {Function} props.onEdit - Función para editar el evento
 */
const HealthEventItem = ({ event, onEdit }) => {
  // Determinar el icono según la categoría
  const getCategoryIcon = (category) => {
    switch(category) {
      case 'physical':
        return '🏃‍♂️';
      case 'cognitive':
        return '🧠';
      case 'emotional':
        return '😊';
      case 'medication':
        return '💊';  // Nuevo icono para medicación
      case 'autonomy':
        return '🦾';
      default:
        return '📋';
    }
  };

  // Formatear fecha de formato ISO a DD/MM/YY
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return `${date.getDate().toString().padStart(2, '0')}/${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getFullYear().toString().slice(2)}`;
  };

  return (
    <div className="health-event-item">
      <div className="event-icon">
        <span>{getCategoryIcon(event.category)}</span>
      </div>
      
      <div className="event-content">
        <div className="event-header">
          <span className="event-category">{event.categoryName}</span>
          <span className="event-date">{formatDate(event.date)}</span>
        </div>
        
        <div className="event-description">
          "{event.description}"
        </div>
      </div>
      
      <button 
        className="edit-button"
        onClick={() => onEdit(event)}
        aria-label="Editar evento"
      >
        editar
      </button>
    </div>
  );
};

export default HealthEventItem;