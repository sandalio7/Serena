import React from 'react';
import HealthEventItem from './HealthEventItem';
import './HealthEventsList.css';

/**
 * Componente de lista de eventos del historial de salud
 * @param {Object} props - Propiedades del componente
 * @param {Array} props.events - Lista de eventos de salud
 * @param {Function} props.onEditEvent - Función para editar un evento
 */
const HealthEventsList = ({ events, onEditEvent }) => {
  return (
    <div className="health-events-list">
      {events.length > 0 ? (
        events.map(event => (
          <HealthEventItem 
            key={event.id}
            event={event}
            onEdit={onEditEvent}
          />
        ))
      ) : (
        <div className="no-events">
          <p>No hay datos para el período seleccionado</p>
        </div>
      )}
    </div>
  );
};

export default HealthEventsList;