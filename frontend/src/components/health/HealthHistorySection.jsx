// HealthHistorySection.jsx - ACTUALIZADO
import React, { useState, useEffect } from 'react';
import HistoryTabs from './HistoryTabs';
import HealthEventItem from './HealthEventItem';
import './HealthHistorySection.css';

/**
 * Componente de sección de historial de salud
 * @param {Object} props - Propiedades del componente
 * @param {Array} props.events - Lista de eventos de salud
 * @param {Function} props.onEditEvent - Función para editar un evento
 * @param {string} props.activePeriod - Período activo
 * @param {Function} props.setActivePeriod - Función para cambiar el período
 * @param {string} props.activeCategory - Categoría activa
 * @param {Function} props.setActiveCategory - Función para cambiar la categoría
 */
const HealthHistorySection = ({ 
  events, 
  onEditEvent, 
  activePeriod, 
  setActivePeriod, 
  activeCategory, 
  setActiveCategory 
}) => {
  const [filteredEvents, setFilteredEvents] = useState([]);
  
  // Efecto para filtrar eventos cuando cambian los filtros o los eventos
  useEffect(() => {
    const filterEvents = () => {
      // Obtener fecha límite según el período seleccionado
      const now = new Date();
      let limitDate = new Date();
      
      switch(activePeriod) {
        case 'day':
          limitDate.setDate(now.getDate() - 1);
          break;
        case 'week':
          limitDate.setDate(now.getDate() - 7);
          break;
        case 'month':
          limitDate.setMonth(now.getMonth() - 1);
          break;
        case 'custom':
          // En caso real, aquí se usaría un selector de fechas
          limitDate.setMonth(now.getMonth() - 3);
          break;
        default:
          limitDate.setDate(now.getDate() - 1);
      }
      
      // Filtrar por período y categoría
      const filtered = events.filter(event => {
        const eventDate = new Date(event.date);
        const matchesPeriod = eventDate >= limitDate;
        const matchesCategory = activeCategory === 'all' || event.category === activeCategory;
        
        return matchesPeriod && matchesCategory;
      });
      
      // Ordenar por fecha (más reciente primero)
      filtered.sort((a, b) => new Date(b.date) - new Date(a.date));
      
      setFilteredEvents(filtered);
    };
    
    filterEvents();
  }, [events, activePeriod, activeCategory]);
  
  return (
    <div className="health-history-section">
      <HistoryTabs 
        activePeriod={activePeriod}
        onPeriodChange={setActivePeriod}
        activeCategory={activeCategory}
        onCategoryChange={setActiveCategory}
      />
      
      <div className="events-container">
        {filteredEvents.length > 0 ? (
          filteredEvents.map(event => (
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
    </div>
  );
};

export default HealthHistorySection;