import React from 'react';
import './PeriodTabs.css';

/**
 * Componente de pestañas para filtrar el historial por período
 * @param {Object} props - Propiedades del componente 
 * @param {string} props.activePeriod - Período activo (day, week, month, custom)
 * @param {Function} props.onPeriodChange - Función para cambiar el período
 */
const PeriodTabs = ({ activePeriod, onPeriodChange }) => {
  return (
    <div className="period-tabs-card">
      <div className="period-tabs">
        <button 
          className={`period-tab ${activePeriod === 'day' ? 'active' : ''}`}
          onClick={() => onPeriodChange('day')}
        >
          Último Día
        </button>
        <button 
          className={`period-tab ${activePeriod === 'week' ? 'active' : ''}`}
          onClick={() => onPeriodChange('week')}
        >
          Última Semana
        </button>
        <button 
          className={`period-tab ${activePeriod === 'month' ? 'active' : ''}`}
          onClick={() => onPeriodChange('month')}
        >
          Último Mes
        </button>
        <button 
          className={`period-tab ${activePeriod === 'custom' ? 'active' : ''}`}
          onClick={() => onPeriodChange('custom')}
        >
          Elegir
        </button>
      </div>
    </div>
  );
};

export default PeriodTabs;