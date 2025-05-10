import React, { useState, useEffect } from 'react';
import PeriodTabs from './PeriodTabs';
import CategoryTabs from './CategoryTabs';
import HealthEventsList from './HealthEventsList';
import './HealthHistorySection.css';

/**
 * Componente de sección de historial de salud
 * @param {Object} props - Propiedades del componente
 * @param {Array} props.events - Lista de eventos de salud
 * @param {Function} props.onEditEvent - Función para editar un evento
 */
const HealthHistorySection = ({ events, onEditEvent }) => {
  // Estados para los filtros activos
  const [activePeriod, setActivePeriod] = useState('day');
  const [activeCategory, setActiveCategory] = useState('all');
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
      
      setFilteredEvents(filtered);
    };
    
    filterEvents();
  }, [events, activePeriod, activeCategory]);
  
  // Transformar nombre de categoría para mostrar
  const getCategoryName = (category) => {
    const categoryMap = {
      'physical': 'Estado Físico',
      'cognitive': 'Estado cognitivo',
      'emotional': 'Estado Emocional',
      'autonomy': 'Autonomía'
    };
    
    return categoryMap[category] || category;
  };
  
  // Añadir nombre de categoría a cada evento
  const eventsWithNames = filteredEvents.map(event => ({
    ...event,
    categoryName: getCategoryName(event.category)
  }));
  
  return (
    <div className="health-history-section">
      <PeriodTabs 
        activePeriod={activePeriod}
        onPeriodChange={setActivePeriod}
      />
      
      <CategoryTabs 
        activeCategory={activeCategory}
        onCategoryChange={setActiveCategory}
      />
      
      <HealthEventsList 
        events={eventsWithNames}
        onEditEvent={onEditEvent}
      />
    </div>
  );
};

export default HealthHistorySection;